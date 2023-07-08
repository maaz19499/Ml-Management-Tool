import hyperopt
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import accuracy_score
import numpy as np
from .config import constant

class RunOpt:
    def __init__(self,algo
                        ,search_space_df
                        ,xtrain
                        ,ytrain
                        ,xtest=None
                        ,ytest=None
                        ,max_iter=10
                        ,class_label=1
                        ,score_metrics=accuracy_score
                        ,score_to_calc_on='Train'
                        ,weight_type ='inalgo'
                        ,verbose=False) -> None:
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xtest=xtest
        self.ytest=ytest
        self.max_trials = max_iter
        self.algo=algo
        self.space_df=search_space_df
        self.metric= score_metrics
        self.verbos=verbose
        self.class_label=class_label
        self.score_to_calc_on=score_to_calc_on
        self.weight_type =weight_type
    
    def get_score(self,model):
        if self.score_to_calc_on=='Train':
            if (self.xtrain is None) | (self.ytrain is None):
                raise ValueError('Train data is missing')
            else:
                pred=model.predict(self.xtrain)
                score = self.metric(self.ytrain, pred)
        else:
            if (self.xtest is None) | (self.ytest is None):
                raise ValueError('Test data is missing')
            else:
                pred = model.predict(self.xtest)
                score = self.metric(self.ytest, pred)

        return(score)

    def fit_model(self,param,pos_wt):
        if pos_wt is not None:
            assert (pos_wt>0) & (pos_wt<1),'Class weight should be between 0 and 1'
            if self.weight_type=='inalgo': # sklearn accept class weights inside algo call
                if 'pos_weight' in param:
                    del param['pos_weight']
                other_class = 0 if self.class_label==1 else 1
                weight = {self.class_label:pos_wt,other_class:1-pos_wt}
                model = self.algo(**param,class_weight=weight)
                model.fit(self.xtrain, self.ytrain)
            else: # xgboost or other external models supports class weight in fit method
                weight = np.where(self.ytrain==self.class_label,pos_wt,1-pos_wt)
                model = self.algo(**param)
                model.fit(self.xtrain, self.ytrain ,sample_weight =weight )
        else:
            model = self.algo(**param)
            model.fit(self.xtrain, self.ytrain)
        return(model)

    def objective(self,params):
        param = {}
        pos_wt = None
        for k,v in params.items():
            if k=='pos_weight':
                pos_wt=v[0] # this a tuple where we have value and its dtype
                continue
            param[k]=int(v[0]) if v[1]=='int' else v[0]
        model =self.fit_model(param=param,pos_wt=pos_wt)

        score = self.get_score(model)
        
        if self.verbos:
            print()
            print ("SCORE:", score)
        return {'loss': -score, 'status': STATUS_OK, 'model': model}

    def create_hp_space(self):
        hp_space = {}
        for idx, a in self.space_df.iterrows():
            dist_fun = constant.distribution_map.get(a['distribution'])
            if a['distribution'][0]=='q':
                pr = {a['Param']:[dist_fun(a['Param'],a['min'],a['max'],a['interval']),a['dtype']]}
     
            else:
                pr = {a['Param']:[dist_fun(a['Param'],a['min'],a['max']),a['dtype']]}
            hp_space.update(pr)
        return(hp_space)

    def get_best_param(self):
        search_space = self.create_hp_space()
        trials = Trials()
        best = fmin(fn=self.objective,
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=self.max_trials,
                    trials=trials)
        best_param = {}
        for k,v in best.items():
            best_param[k]=int(v) if search_space[k][1]=='int' else v
        return(best_param)

    def run_exp(self):
        best_params = self.get_best_param()
        # print(best_params)
        model = self.fit_model(param=best_params,pos_wt = best_params['pos_weight'])
        return model,best_params
        

    