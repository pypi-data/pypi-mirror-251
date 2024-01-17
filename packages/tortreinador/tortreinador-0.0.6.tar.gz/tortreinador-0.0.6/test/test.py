import pandas as pd
from tortreinador import train
from tortreinador.utils.preprocessing import load_data
import torch
from tortreinador.models.MDN import mdn, Mixture, NLLLoss
from tortreinador.utils.plot import plot_line_2

data = pd.read_excel('D:\\Resource\\Gas_Giants_Core_Earth20W.xlsx')
data['M_total (M_E)'] = data['Mcore (M_J/10^3)'] + data['Menv (M_E)']

input_parameters = [
    'Mass (M_J)',
    'Radius (R_E)',
    'T_sur (K)',
]

output_parameters = [
    'M_total (M_E)',
    'T_int (K)',
    'P_CEB (Mbar)',
    'T_CEB (K)'
]

trainer = train.TorchTrainer(epoch=10)

t_loader, v_loader, test_x, test_y, s_x, s_y = load_data(data=data, input_parameters=input_parameters,
                                                         output_parameters=output_parameters,
                                                         if_normal=True, if_shuffle=True, batch_size=512)

model = mdn(len(input_parameters), len(output_parameters), 10, 256)
criterion = NLLLoss()
pdf = Mixture()
optim = torch.optim.Adam(model.parameters(), lr=0.0001984)

t_l, v_l, val_r2, train_r2, mse = trainer.fit_for_MDN(t_loader, v_loader, criterion, model=model, mixture=pdf,
                                                      model_save_path='D:\\Resource\\MDN\\', optim=optim, best_r2=0.9)


result_pd = pd.DataFrame()
result_pd['epoch'] = range(10)
result_pd['train_r2_avg'] = train_r2
result_pd['val_r2_avg'] = val_r2

plot_line_2(y_1='train_r2_avg', y_2='val_r2_avg', df=result_pd, fig_size=(10, 6), output_path="D:\\PythonProject\\RebuildProject\\Rock\\imgs\\Test_TrainValR2.png", dpi=300)

