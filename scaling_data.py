import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 받은 데이터 인덱스정리
def make_df(df):
    df.set_index(['WEARABLE_ID', "TIME"], drop=False, inplace=True)
    df.drop(['WEARABLE_ID'], axis=1, inplace=True)
    df.drop(['TIME'], axis=1, inplace=True)
    df = df.sort_index(ascending=True)

    return df

# 데이터 스케일 및 스케일러 저장
def data_scaler(df):
    count = 0
    k = 0

    scaled_diastolic_array = np.empty((0, 1), dtype=float)
    scaler_diastolic_list = []

    scaled_systolic_array = np.empty((0, 1), dtype=float)
    scaler_systolic_list = []

    scaled_stress_array = np.empty((0, 1), dtype=float)
    scaler_stress_list = []

    scaled_spo2_array = np.empty((0, 1), dtype=float)
    scaler_spo2_list = []

    for i in range(len(df.index)):
        if i < (len(df.index) - 1):
            if not df.index[i][0] == df.index[i + 1][0]:
                count = count + 1

                # DIASTOLIC
                scaled_diastolic = df["DIASTOLIC"][k:i + 1]
                globals()['scaler_diastolic_{}'.format(count)] = MinMaxScaler()
                scaled_diastolic_array = np.append(scaled_diastolic_array,
                                                   globals()['scaler_diastolic_{}'.format(count)].fit_transform(
                                                       (scaled_diastolic.values).reshape(-1, 1)),
                                                   axis=0)
                scaler_diastolic_list.append(globals()['scaler_diastolic_{}'.format(count)])

                # SYSTOLIC
                scaled_systolic = df["SYSTOLIC"][k:i + 1]
                globals()['scaler_systolic_{}'.format(count)] = MinMaxScaler()
                scaled_systolic_array = np.append(scaled_systolic_array,
                                                  globals()['scaler_systolic_{}'.format(count)].fit_transform(
                                                      (scaled_systolic.values).reshape(-1, 1)),
                                                  axis=0)

                scaler_systolic_list.append(globals()['scaler_systolic_{}'.format(count)])

                # STRESS
                scaled_stress = df["STRESS"][k:i + 1]
                globals()['scaler_stress_{}'.format(count)] = MinMaxScaler()
                scaled_stress_array = np.append(scaled_stress_array,
                                                globals()['scaler_stress_{}'.format(count)].fit_transform(
                                                    (scaled_stress.values).reshape(-1, 1)),
                                                axis=0)

                scaler_stress_list.append(globals()['scaler_stress_{}'.format(count)])

                # SPO2
                scaled_spo2 = df["SPO2"][k:i + 1]
                globals()['scaler_spo2_{}'.format(count)] = MinMaxScaler()
                scaled_spo2_array = np.append(scaled_spo2_array,
                                              globals()['scaler_spo2_{}'.format(count)].fit_transform(
                                                  (scaled_spo2.values).reshape(-1, 1)),
                                              axis=0)

                scaler_spo2_list.append(globals()['scaler_spo2_{}'.format(count)])

                k = i + 1

        else:
            count = count + 1

            # DIASTOLIC
            scaled_diastolic = df["DIASTOLIC"][k:i + 1]
            globals()['scaler_diastolic_{}'.format(count)] = MinMaxScaler()
            scaled_diastolic_array = np.append(scaled_diastolic_array,
                                               globals()['scaler_diastolic_{}'.format(count)].fit_transform(
                                                   (scaled_diastolic.values).reshape(-1, 1)),
                                               axis=0)
            scaler_diastolic_list.append(globals()['scaler_diastolic_{}'.format(count)])

            # SYSTOLIC
            scaled_systolic = df["SYSTOLIC"][k:i + 1]
            globals()['scaler_systolic_{}'.format(count)] = MinMaxScaler()
            scaled_systolic_array = np.append(scaled_systolic_array,
                                              globals()['scaler_systolic_{}'.format(count)].fit_transform(
                                                  (scaled_systolic.values).reshape(-1, 1)),
                                              axis=0)

            scaler_systolic_list.append(globals()['scaler_systolic_{}'.format(count)])

            # STRESS
            scaled_stress = df["STRESS"][k:i + 1]
            globals()['scaler_stress_{}'.format(count)] = MinMaxScaler()
            scaled_stress_array = np.append(scaled_stress_array,
                                            globals()['scaler_stress_{}'.format(count)].fit_transform(
                                                (scaled_stress.values).reshape(-1, 1)),
                                            axis=0)

            scaler_stress_list.append(globals()['scaler_stress_{}'.format(count)])

            # SPO2
            scaled_spo2 = df["SPO2"][k:i + 1]
            globals()['scaler_spo2_{}'.format(count)] = MinMaxScaler()
            scaled_spo2_array = np.append(scaled_spo2_array,
                                          globals()['scaler_spo2_{}'.format(count)].fit_transform(
                                              (scaled_spo2.values).reshape(-1, 1)),
                                          axis=0)

            scaler_spo2_list.append(globals()['scaler_spo2_{}'.format(count)])

            k = i + 1

    scaled_diastolic_array = scaled_diastolic_array.reshape(-1, )
    scaled_systolic_array = scaled_systolic_array.reshape(-1, )
    scaled_stress_array = scaled_stress_array.reshape(-1, )
    scaled_spo2_array = scaled_spo2_array.reshape(-1, )

    scaled_df = pd.DataFrame({'DIASTOLIC': scaled_diastolic_array,
                              'SYSTOLIC': scaled_systolic_array,
                              'STRESS': scaled_stress_array,
                              'SPO2': scaled_spo2_array})

    return scaled_df, scaler_diastolic_list, scaler_systolic_list, scaler_stress_list, scaler_spo2_list

# 예측된 값 재변환
def inverse_data(pred_output, future_target, scaler_diastolic_list, scaler_systolic_list, scaler_stress_list,
                 scaler_spo2_list):
    output_t = pred_output.detach().numpy()

    predict_dia = []
    predict_sys = []
    predict_str = []
    predict_spo = []

    for i in range(len(output_t)):
        for j in range(len(output_t[0])):
            predict_dia.append(output_t[i][j][0])
            predict_sys.append(output_t[i][j][1])
            predict_str.append(output_t[i][j][2])
            predict_spo.append(output_t[i][j][3])

    predict_dia = np.array(predict_dia).reshape(-1, 1)
    predict_sys = np.array(predict_sys).reshape(-1, 1)
    predict_str = np.array(predict_str).reshape(-1, 1)
    predict_spo = np.array(predict_spo).reshape(-1, 1)

    inv_pred_dia = []
    inv_pred_sys = []
    inv_pred_str = []
    inv_pred_spo = []

    for i in range(1):
        inv_pred_dia = scaler_diastolic_list[i].inverse_transform(predict_dia[0:future_target])
        inv_pred_sys = scaler_systolic_list[i].inverse_transform(predict_sys[0:future_target])
        inv_pred_str = scaler_stress_list[i].inverse_transform(predict_str[0:future_target])
        inv_pred_spo = scaler_spo2_list[i].inverse_transform(predict_spo[0:future_target])

        inv_pred_dia = inv_pred_dia.astype(int)
        inv_pred_sys = inv_pred_sys.astype(int)
        inv_pred_str = inv_pred_str.astype(int)
        inv_pred_spo = inv_pred_spo.astype(int)

        inv_pred_dia = np.ravel(inv_pred_dia, order='C').tolist()
        inv_pred_sys = np.ravel(inv_pred_sys, order='C').tolist()
        inv_pred_str = np.ravel(inv_pred_str, order='C').tolist()
        inv_pred_spo = np.ravel(inv_pred_spo, order='C').tolist()

    bp_score = []
    for i in range(len(inv_pred_dia)):
        dia_score = abs(inv_pred_dia[i] - 80) / 20
        sys_score = abs(inv_pred_sys[i] - 120) / 30
        bp_score.append((dia_score + sys_score) * 50)
        bp_score = list(map(int, bp_score))

    return bp_score, inv_pred_str, inv_pred_spo
