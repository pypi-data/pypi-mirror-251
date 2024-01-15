from loguru import logger

from sybil_engine.config.app_config import get_okx
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.utils.accumulator import add_accumulator_str
from sybil_engine.utils.okx import withdrawal, SUPPORTED_OKX_WITHDRAWAL
from sybil_engine.utils.utils import randomized_sleeping, ModuleException, AccountException, print_exception_chain


class ModuleExecutor:

    def __init__(self, sleep_interval):
        self.sleep_interval = sleep_interval

    def execute_modules(self, modules, account):
        try:
            for module, module_args in modules:
                self.execute_module(module_args, account, module)
        except AccountException as e:
            logger.error(f'Error, skip {account}:')
            print_exception_chain(e)
            add_accumulator_str("Failed accounts: ", account)
        except Exception as e:
            logger.error(f'Error, skip {account}:')
            print_exception_chain(e)
            add_accumulator_str("Failed accounts: ", account)

    def execute_module(self, module_args, account, module):
        try:
            parsed_module_args = module.parse_params(module_args)
            try:
                module.execute(*parsed_module_args, account)
                if module.sleep_after():
                    randomized_sleeping(self.sleep_interval)
            except Exception as e:
                module.handle(e)
        except ModuleException as e:
            print_exception_chain(e)
        except NotEnoughNativeBalance as e:
            okx_secret, (cex_data, auto_withdrawal, min_auto_withdraw_interval, withdraw_interval) = get_okx()

            chain_instance = get_chain_instance(e.chain)

            if auto_withdrawal and e.chain in SUPPORTED_OKX_WITHDRAWAL and module.auto_withdrawal:
                withdrawal(account.address, okx_secret, e.chain, cex_data, withdraw_interval, chain_instance['gas_token'])
                randomized_sleeping({'from': 60 * 5, 'to': 60 * 10})
                self.execute_module(module_args, account, module)
            else:
                raise AccountException(e) from e
