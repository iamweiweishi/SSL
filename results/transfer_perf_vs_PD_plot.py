import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

fpath = './full_data.csv'
df_full_data = pd.read_csv(fpath, index_col = False)
dict_full_data = df_full_data.set_index('Models').to_dict()

# TO DO:
# 1. add stoic and imagenet PD to full_data.csv
# 2. plot for transfer_setting in ['few shot', 'finetune', 'linear'] - DONE
# 3. plot for transfer_setting == 'average' (i.e average across settings)
# 4. save plots in relevant directory

def plot_dset_acc_vs_pd(transfer_setting, dset_name):
    '''
    transfer_setting in ['few shot', 'finetune', 'linear', 'average']
    dset_name in ['shenzhencxr','montgomerycxr','bach',
                  'iChallengeAMD', 'iChallengePM','chexpert',
                  'stoic','diabetic retinopathy (5way)', 
                  'chestx (5way)', 'cifar10 (2way)']
    '''
    if transfer_setting == 'average':
        try:
            few_shot_acc_column_name = 'few shot ' + dset_name
            few_shot_dset_acc_dict = dict_full_data[few_shot_acc_column_name]

            finetune_acc_column_name = 'finetune ' + dset_name
            finetune_dset_acc_dict = dict_full_data[finetune_acc_column_name]

            linear_acc_column_name = 'linear ' + dset_name
            linear_dset_acc_dict = dict_full_data[linear_acc_column_name]

            shared_dsets = few_shot_dset_acc_dict.keys() and finetune_dset_acc_dict.keys() and linear_dset_acc_dict.keys()
            dset_acc_dict = {k: (few_shot_dset_acc_dict[k]+finetune_dset_acc_dict[k]+linear_dset_acc_dict[k])/3 for k in shared_dsets}
        except KeyError:
            print('This dataset does not have data for all linear, few-shot and finetune settings.')
            raise

    else:
        acc_column_name = transfer_setting + ' ' + dset_name
        dset_acc_dict = dict_full_data[acc_column_name]

    for architecture in ['AlexNet', 'VGG', 'SqueezeNet']:

        PD_column_name = f'perceptual distance {architecture.lower()} {dset_name}'
        architecture_dict = dict_full_data[PD_column_name]

        shared_models = dset_acc_dict.keys() and architecture_dict.keys()
        dict_intersection = {k: (dset_acc_dict[k], architecture_dict[k]) for k in shared_models}
        new_df = pd.DataFrame.from_dict(dict_intersection, orient='index')
        new_df = new_df.reset_index(level=0)
        new_df.columns = ['model', f'{transfer_setting}', 'perceptual_distance']

        sns.set_style("darkgrid")
        markers=['o', 'x', 'D', 's', '<', '>', 'v', 'X', '+', 'P', '4', 'p', '|']  # added 'o' to plot simclr-v1
        g = sns.lmplot(x=f'{transfer_setting}', y="perceptual_distance", hue="model", data=new_df, fit_reg=False, markers=markers, palette="tab10", scatter_kws={"s": 150})
        sns.regplot(x=f'{transfer_setting}', y="perceptual_distance", data=new_df, scatter=False, ax=g.axes[0, 0])
        plt.ylabel(f"Perceptual Distance ({architecture})")
        plt.xlabel(f"{transfer_setting.title()} Accuracy")
        plt.title(dset_name)
        plt.show()


plot_dset_acc_vs_pd('few shot', 'shenzhencxr')