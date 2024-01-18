from datetime import datetime
from aiohttp import http_websocket
from monstr.relay.exceptions import NostrCommandException, NostrNoticeException, NostrNotAuthenticatedException
from monstr.event.event import Event
from monstr.util import util_funcs, NIPSupport



class AcceptReqHandler:
    """
        request handler for relay, a request handler just has to have
        accept_post(self, ws: WebSocket, evt: Event) method that throws
        NostrCommandException if we don't want to accept message
    """
    def __init__(self, descriptive_msg=True):
        self._desc_msg = descriptive_msg

    def raise_err(self, event: Event, message: str, success: bool = False):
        if self._desc_msg:
            raise NostrCommandException(event.id, success, message)
        else:
            raise NostrNoticeException('post not accepted')

    def accept_post(self, ws: http_websocket, evt: Event):
        pass


class LengthAcceptReqHandler(AcceptReqHandler):
    """
    use to only accept messages of set lengths, most likely upto a max size
    """
    def __init__(self, min=1, max=None, descriptive_msg=True):
        """
        :param max: accept no longer then this
        :param min: - could be used to stop 0 length messages but maybe should include kind?
        """
        self._min = min
        self._max = max
        super().__init__(descriptive_msg)

    def accept_post(self, ws: http_websocket, evt: Event):
        msg_len = len(evt.content)
        if self._min and msg_len < self._min:
            self.raise_err(event=evt,
                           success=False,
                           message='blocked: content < accepted min %s got %s' % (self._min, msg_len))
        elif self._max and msg_len > self._max:
            self.raise_err(event=evt,
                           success=False,
                           message='blocked: content > accepted max %s got %s' % (self._max, msg_len))

    def __str__(self):
        return 'LengthAcceptReqHandler (%s-%s)' % (self._min, self._max)


class ThrottleAcceptReqHandler(AcceptReqHandler):
    """
    keeps track of time of messages for each pub_key and only lets repost if enough time has passed since
    last post
    maybe secs is too long change to use dt.timestamp() directly and then can do decimal point for parts of sec?

    """
    def __init__(self, tick_min=1, descriptive_msg=True):
        """
        :param tick_min: secs before a post is allowed per pub key
        :param descriptive_msg:
        """
        self._tickmin = tick_min
        # pub_key to last eventtime, NOTE never cleaned down at the moment
        self._track = {}
        super().__init__(descriptive_msg)

    def accept_post(self, ws: http_websocket, evt: Event):
        # pubkey posted before
        if evt.pub_key in self._track:
            # time since last post
            dt = util_funcs.date_as_ticks(datetime.now())-self._track[evt.pub_key]
            # time since last event is not enough msg not accepted
            if dt < self._tickmin:
                # update time anyway, this means if keep posting will keep failing...
                self._track[evt.pub_key] = util_funcs.date_as_ticks(datetime.now())
                self.raise_err(event=evt,
                               success=False,
                               message='blocked: pubkey %s posted too recently, posts most be %ss apart' % (evt.pub_key,
                                                                                                            self._tickmin))

        # update last post for pubkey
        self._track[evt.pub_key] = util_funcs.date_as_ticks(datetime.now())


class CreateAtAcceptor(AcceptReqHandler, NIPSupport):
    """
        implements create_at range acceptance as NIP22
        https://github.com/nostr-protocol/nips/blob/master/22.md
    """
    def __init__(self,
                 max_before:int = None,
                 max_after:int = None,
                 descriptive_msg=True):
        self._max_before = max_before
        self._max_after = max_after

        # one should be set but just incase
        if self._max_after or self._max_before:
            NIPSupport.__init__(self,
                                nip22=True)
        super().__init__(descriptive_msg)

    def accept_post(self, ws: http_websocket, evt: Event):
        now = util_funcs.date_as_ticks(datetime.now())
        evt_time = evt.created_at_ticks
        if self._max_before:
            min_accept = now - self._max_before
            if min_accept > evt_time:
                self.raise_err(event=evt,
                               success=False,
                               message=f'blocked: event time is too early, event created_at: {evt_time} - min accepted: {min_accept}')
        if self._max_after:
            max_accept = now + self._max_after
            if max_accept < evt_time:
                self.raise_err(event=evt,
                               success=False,
                               message=f'blocked: event time is too late, event created_at: {evt_time} - max accepted: {max_accept}')


class AuthenticatedAcceptor(AcceptReqHandler, NIPSupport):
    """
        basic implementation of acceptor that only accepts from certain authenticated pub keys
        https://github.com/nostr-protocol/nips/blob/master/42.md

        relay must also _request_auth True otherwise auth requests won't get sent so no-one will
        ever get authenticated
    """
    def __init__(self,
                 authorised_keys: set | list | None = None,
                 descriptive_msg=True):

        # hex pubkeys to accept - probably we should also accept [Keys] maybe even Profiles?
        # can also set None, which will allow all so long as they authenticated an event
        self.authorised_keys = authorised_keys

        NIPSupport.__init__(self,
                            nip42=True
                            )
        super().__init__(descriptive_msg)

    @property
    def authorised_keys(self) -> set:
        return self._authorised_keys

    @authorised_keys.setter
    def authorised_keys(self, authorised_keys: list | set | None = None):
        if isinstance(authorised_keys, list):
            authorised_keys = set(authorised_keys)
        self._authorised_keys = authorised_keys

    def accept_post(self, ws: http_websocket, evt: Event):
        try:
            ret = evt.pub_key in ws.authenticated_pub_ks

            # authenticated but not for key of the given event
            if ret is False:
                raise NostrNotAuthenticatedException(f'restricted: user {evt.pub_key} not yet authenticated')

            # if authorised_keys is None then anyone can post so long as they authorised
            # otherwise evt.pub_key must be in authorised_keys
            ret = self.authorised_keys is None or \
                  evt.pub_key in self.authorised_keys

            if ret is False:
                self.raise_err(event=evt,
                               success=False,
                               message=f'restricted: user {evt.pub_key} authenticated but not allowed')

        # no authentication done at all yet?
        except AttributeError as ae:
            raise NostrNotAuthenticatedException(f'restricted: user {evt.pub_key} not yet authenticated')


        return ret


