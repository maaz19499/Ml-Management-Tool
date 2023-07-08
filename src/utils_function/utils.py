import os
import yaml
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from sklearn.metrics import confusion_matrix, accuracy_score,f1_score,classification_report
from sklearn.metrics import recall_score,ConfusionMatrixDisplay,roc_auc_score,auc

def load_yaml(dir,file_name):

    path = os.path.join(dir,file_name)
    assert os.path.exists(path),f'Given YAML file {file_name} is not at {dir}'

    config={}

    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return(config)

def show_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_pagination(paginationPageSize=10,paginationAutoPageSize=False)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_default_column(groupable=True, value=True
                    , enableRowGroup=False, aggFunc="sum", editable=True,min_column_width=5)
    gridOptions = gb.build()
    grid_data = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True
                        ,update_mode=GridUpdateMode.SELECTION_CHANGED)
    return(grid_data)

def performance(model,X,Y):
    print('Performance')
    pred = model.predict(X)
    print(pred)
    prob = model.predict_proba(X)[:,1]
    print('after proba')
    cm = confusion_matrix(Y.values,pred)
    acc = accuracy_score(Y.values,pred)
    f1 = f1_score(Y,pred)
    clf_report = classification_report(Y,pred)
    roc_score = roc_auc_score(Y.values,prob)
    return cm,acc,f1,clf_report,roc_score
