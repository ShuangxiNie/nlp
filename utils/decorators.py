from functools import wraps
from typing import Callable, TypeVar, Any, ParamSpec
from inspect import signature, Parameter

P = ParamSpec('P')
R = TypeVar('R')

def required_params(*param_names: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    检查必需参数的装饰器
    
    Args:
        param_names: 必需参数名列表
        
    Example:
        @required_params('user_id', 'amount')
        def transfer_money(user_id: int, amount: float): ...
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        sig = signature(func)
        
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            missing = [
                name for name in param_names 
                if name not in bound.arguments or bound.arguments[name] is None
            ]
            if missing:
                raise ValueError(f"Missing required parameters: {', '.join(missing)}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator