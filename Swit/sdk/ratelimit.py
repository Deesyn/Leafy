import json
from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@dataclass
class RateLimitData:
    data: Dict[int, float] = field(default_factory=dict)

class ratelimit:
    @staticmethod
    def Add(
            user_id: int,
            timeout: int = 30,
            auto_reset: bool = False,
            max_actions: int = 1,
            reset_on_action: bool = False,
            now: float | None = None
    ):
        rate = RateLimitData()
        if user_id not in rate.data:
            temp_data = {
                "user_id": user_id,
                "timestamp": get_timestamp(),
                "time_out": timeout,
                "auto_reset": auto_reset,
                "max_actions": max_actions,
                "reset_on_action": reset_on_action,
                "now": now if now else now
            }
            parser = json.loads(temp_data)
            rate.data[user_id] = parser
            returnData = {
                "status_code": 1,
                "description": "Success",
            }
            return returnData
        else:
            returnData = {
                "status_code": 2,
                "description": "the user is already in the ratelimit list"
            }
            return returnData
    @staticmethod
    def Check(user_id:int):
        pass
    @staticmethod
    def Reset():
        pass
