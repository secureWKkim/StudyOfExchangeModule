from abc import ABC, abstractmethod


class Machine(ABC):
    @abstractmethod
    def get_filled_orders(self):
        """체결 정보를 구함"""
        pass

    @abstractmethod
    def get_ticker(self):
        """마지막 체결 정보(Tick)를 구함"""
        pass

    @abstractmethod
    def get_wallet_status(self):
        """사용자 지갑 정보를 조회"""
        pass

    @abstractmethod
    def get_token(self):
        """액세스 토큰 정보를 구함"""
        pass

    @abstractmethod
    def set_token(self):
        """액세스 토큰 정보를 만듦"""
        pass

    @abstractmethod
    def get_username(self):
        """현재 사용자 이름을 구함"""
        pass

    @abstractmethod
    def buy_order(self):
        """매수 주문 실행"""
        pass

    @abstractmethod
    def sell_order(self):
        """매도주문 실행"""
        pass

    @abstractmethod
    def cancel_order(self):
        """취소주문 실행"""
        pass

    @abstractmethod
    def get_my_order_status(self):
        """사용자의 주문 상세 정보를 조회"""
        pass