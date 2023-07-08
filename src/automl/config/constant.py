from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

# Prameter Settings
# http://hyperopt.github.io/hyperopt/getting-started/search_spaces/
distribution_map ={# 'choice':hp.choice, # we are not supporting choice as of now.
                        # 'randint':hp.randint,
                        'uniform':hp.uniform
                        ,'quniform':hp.quniform
                        ,'loguniform':hp.loguniform
                        ,'qloguniform':hp.qloguniform
                        ,'normal':hp.normal
                        ,'qnormal':hp.qnormal
                        ,'lognormal':hp.lognormal
                        ,'qlognormal':hp.qlognormal
                        }
default_params_range=['min','max','interval','dist','dtype']

# Algo Params Settings
algo_supported =['XG Boost','Random Forest']
algo_params_file =['xgbparams.yaml','rfparams.yaml']
algo_params_default_file =['default_xgbparams.yaml','default_rfparams.yaml']

