import torch
import pandas as pd
import requests
import io
import scaling_data
import request_moduel
import datetime
import time

def main():
    class LTSF_NLinear(torch.nn.Module):
        def __init__(self, window_size, forcast_size, individual, feature_size):
            super(LTSF_NLinear, self).__init__()
            self.window_size = window_size
            self.forcast_size = forcast_size
            self.individual = individual
            self.channels = feature_size
            if self.individual:
                self.Linear = torch.nn.ModuleList()
                for i in range(self.channels):
                    self.Linear.append(torch.nn.Linear(self.window_size, self.forcast_size))
            else:
                self.Linear = torch.nn.Linear(self.window_size, self.forcast_size)

        def forward(self, x):
            seq_last = x[:, -1:, :].detach()
            x = x - seq_last
            if self.individual:
                output = torch.zeros([x.size(0), self.forcast_size, x.size(2)], dtype=x.dtype).to(x.device)
                for i in range(self.channels):
                    output[:, :, i] = self.Linear[i](x[:, :, i])
                x = output
            else:
                x = self.Linear(x.permute(0, 2, 1)).permute(0, 2, 1)
            x = x + seq_last
            return x

    #윈도우 설정
    shift_days = 3
    shift_steps = shift_days * 24
    future_target = 12

    #모델 불러오기
    model_serv = LTSF_NLinear(window_size=shift_steps, forcast_size=future_target, individual=False, feature_size=1)
    model_serv.load_state_dict(torch.load('health_NLinear2.pth'))

    headers = {
        'X-Auth-token': '<JWT_TOKEN_REMOVED>', }
    today = datetime.datetime.now()
    past = today + datetime.timedelta(days=-90)
    today_str = today.strftime('%Y-%m-%d %H:00:00')
    past_str = past.strftime('%Y-%m-%d %H:00:00')

    request_user = requests.post("http://HOST:PORT/api/v1/house/user_health_device", headers=headers)
    text_user = request_user.text
    df_user = pd.read_csv(io.StringIO(text_user), sep=',')
    print(len(df_user))
    print(df_user)

    for i in range(len(df_user)):
        user = df_user['WEARABLE_ID'][i]
        text_bp, text_stress, text_spo2 = request_moduel.create_data(headers, user, past_str, today_str)
        df_bp = pd.read_csv(io.StringIO(text_bp), sep=',')
        df_stress = pd.read_csv(io.StringIO(text_stress), sep=',')
        df_spo2 = pd.read_csv(io.StringIO(text_spo2), sep=',')

        print(df_bp)

        if df_bp.shape[1] < 3 or df_stress.shape[1] < 3 or df_spo2.shape[1] < 3:  # 조회가 안될시
            print("1")
            predict_bp = request_moduel.recent_bp(headers, user)
            predict_spo2 = request_moduel.recent_spo2(headers, user)
            predict_stress = request_moduel.recent_stress(headers, user)

            request_moduel.send_bp(headers, user, predict_bp, today_str)
            request_moduel.send_spo2(headers, user, predict_spo2, today_str)
            request_moduel.send_stress(headers, user, predict_stress, today_str)


        else:  # 나머지는 실행
            df_final = pd.DataFrame({
                'WEARABLE_ID': df_bp['WEARABLE_ID'],
                "TIME": df_bp['START_TIME'],
                "DIASTOLIC": df_bp['DIASTOLIC'],
                'SYSTOLIC': df_bp['SYSTOLIC'],
                'STRESS': df_stress['SCORE'],
                'SPO2': df_spo2['SPO2']
            })

            if len(df_final) != 72:
                print("2")
                predict_bp = request_moduel.recent_bp(headers, user)
                predict_spo2 = request_moduel.recent_spo2(headers, user)
                predict_stress = request_moduel.recent_stress(headers, user)

                request_moduel.send_bp(headers, user, predict_bp, today_str)
                request_moduel.send_spo2(headers, user, predict_spo2, today_str)
                request_moduel.send_stress(headers, user, predict_stress, today_str)

            else:
                health_df = scaling_data.make_df(df_final)

                scaled_health, scaler_diastolic_list, scaler_systolic_list, scaler_stress_list, scaler_spo2_list = scaling_data.data_scaler(health_df)
                health_df['DIASTOLIC'] = scaled_health['DIASTOLIC'].values
                health_df['SYSTOLIC'] = scaled_health['SYSTOLIC'].values
                health_df['STRESS'] = scaled_health['STRESS'].values
                health_df['SPO2'] = scaled_health['SPO2'].values

                train_dataset = health_df.values
                train_dataset = train_dataset.reshape(1, 72, 4)
                final_x_data = torch.tensor(train_dataset, dtype=torch.float32)

                output_test = model_serv(final_x_data)
                bp_score, inv_pred_str, inv_pred_spo = scaling_data.inverse_data(output_test, future_target,
                                                                                 scaler_diastolic_list,
                                                                                 scaler_systolic_list,
                                                                                 scaler_stress_list,
                                                                                 scaler_spo2_list)

                request_moduel.send_bp(headers, user, bp_score, today_str)
                request_moduel.send_spo2(headers, user, inv_pred_spo, today_str)
                request_moduel.send_stress(headers, user, inv_pred_str, today_str)

    print(time.strftime('%Y.%m.%d - %H:%M:%S') + "   finish")
if __name__ == '__main__':
    main()
