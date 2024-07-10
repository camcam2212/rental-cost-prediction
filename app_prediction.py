import streamlit as st
from PIL import Image
import pandas as pd
import pickle
import plotly.express as px
import config

class RealEstatePredictor:
    def __init__(self):
        self.model_filename = r'D:\OneDrive\KiotViet\Python_for_work\KFinance\sondn_kfinance\Model_Prediction_RentalCost\model\RandomForestRegressor_rental_cost.pkl'
        self.image_filename = r'D:\OneDrive\KiotViet\Python_for_work\KFinance\sondn_kfinance\Model_Prediction_RentalCost\images\OK2.jpg'
        self.data_filename = r'D:\OneDrive\KiotViet\Python_for_work\KFinance\sondn_kfinance\Model_ShortTerm_Loan\CSV_crawl_data\all_bds_final_clean.csv'
        self.loaded_model = None
        self.city_district_mapping = config.city_district_mapping
        self.city_district_mapping_raw = config.city_district_mapping_raw

    def load_model(self):
        try:
            with open(self.model_filename, 'rb') as file:
                self.loaded_model = pickle.load(file)
        except Exception as e:
            st.error(f"Lỗi khi tải mô hình: {str(e)}")

    def predict_price(self, area_value, district, city, ward, street):
        user_data = pd.DataFrame({'area_value': [area_value], 'City': [city], 'District': [district], 'Ward': [ward], 'Street': [street]})
        prediction = self.loaded_model.predict(user_data)
        return prediction[0]

    def run(self):
        st.set_page_config(layout="wide")
        self.load_model()

        header_image = Image.open(self.image_filename)
        st.image(header_image, use_column_width=True)

        selected_city = st.selectbox("Chọn Tỉnh/Thành phố:", list(self.city_district_mapping.keys()))

        # Danh sách quận/huyện phụ thuộc vào tỉnh/thành phố đã chọn
        selected_districts = list(self.city_district_mapping[selected_city].keys())
        selected_district = st.selectbox("Chọn Quận/Huyện:", selected_districts)

        # Danh sách phường/xã phụ thuộc vào tỉnh/thành phố và quận/huyện đã chọn
        selected_wards = list(self.city_district_mapping[selected_city][selected_district].keys())
        selected_ward = st.selectbox("Chọn Phường/Xã:", selected_wards)

        # Danh sách đường/phố phụ thuộc vào tỉnh/thành phố, quận/huyện và phường/xã đã chọn
        selected_streets = self.city_district_mapping[selected_city][selected_district][selected_ward]
        selected_street = st.selectbox("Chọn Đường/Phố:", selected_streets)

        area_value = st.number_input("Diện tích (m2):", min_value=0.0, value=0.0)

        if st.button("Dự đoán"):
            if self.loaded_model is not None:
                try:
                    prediction = self.predict_price(area_value, selected_district, selected_city, selected_ward, selected_street)
                    st.success(f"Số tiền thuê một tháng là: {prediction:,.0f} triệu VNĐ")
                    # st.success(f"Dự đoán giá mỗi mét vuông là: {prediction:,.0f} VND")
                    # st.success(f"Số tiền thuê một tháng: {area_value * prediction:,.0f} VND")
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")
            else:
                st.error("Lỗi: Không thể tải mô hình. Vui lòng kiểm tra lại.")

        df = pd.read_csv(self.data_filename)
        df_median = df.groupby(['City', 'District'])['price_value_trieu'].median().reset_index()
        df_hcm = df_median[df_median['City'] == selected_city]
        fig = px.bar(df_hcm, x='District', y='price_value_trieu', title=f"Biểu đồ giá theo quận - Thành phố {selected_city}")
        fig.update_layout(xaxis_title='Quận', yaxis_title='Trung vị giá/tháng (triệu)', xaxis_tickangle=-45, width=1200, height=700)
        st.plotly_chart(fig)

        df_median2 = df.groupby(['City','District','Ward'])['price_value_trieu'].median().reset_index()
        df_wardd = df_median2[df_median2['District'] == selected_district]
        fig = px.bar(df_wardd, x='Ward', y='price_value_trieu', title=f"Biểu đồ giá theo Phường - Quận {selected_district} - TP {selected_city}")
        fig.update_layout(xaxis_title='Phường', yaxis_title='Trung vị giá/tháng (triệu)', xaxis_tickangle=-45, width=1200, height=700)
        st.plotly_chart(fig)

        df_median3 = df.groupby(['City','District','Ward','Street'])['price_value_trieu'].median().reset_index()
        df_street = df_median3[df_median3['Street'] == selected_street]
        fig = px.bar(df_street, x='Street', y='price_value_trieu', title=f"Biểu đồ giá theo Phường - Quận {selected_district} - TP {selected_city}")
        fig.update_layout(xaxis_title='Đường', yaxis_title='Trung vị giá/tháng (triệu)', xaxis_tickangle=-45, width=1200, height=700)
        st.plotly_chart(fig)

        # #Tạo danh sách đường/phố thuộc tỉnh/tp
        # selected_city_districts = list(self.city_district_mapping[selected_city].keys())
        # # Tạo DataFrame mới chỉ chứa dữ liệu của các đường/phố thuộc thành phố và quận/huyện đã chọn
        # df_selected_city_districts = df[(df['City'] == selected_city) & (df['District'].isin(selected_city_districts))]
        # # Tính trung vị giá/m2 cho từng đường/phố trong thành phố và quận/huyện đã chọn
        # df_median3 = df_selected_city_districts.groupby(['City', 'District', 'Street'])['price_value_trieu'].mean().reset_index()
        # # Tạo biểu đồ dựa trên DataFrame đã lọc
        # fig = px.bar(df_median3, x='Street', y='price_value_trieu', title=f"Biểu đồ giá/m2 theo Đường - TP {selected_city}")
        # fig.update_layout(xaxis_title='Đường/Phố', yaxis_title='Trung vị giá / m2', xaxis_tickangle=-45, width=1200, height=700)
        # st.plotly_chart(fig)

        # selected_city_streets2 = []
        # for district in self.city_district_mapping[selected_city]:
        #     for ward in self.city_district_mapping[selected_city][district]:
        #         selected_city_streets2.extend(self.city_district_mapping[selected_city][district][ward])
        # # Tạo DataFrame mới chỉ chứa dữ liệu của các đường/phố thuộc thành phố đã chọn
        # df_selected_city_streets = df[df['Street'].isin(selected_city_streets2)]
        # # Tính trung vị giá/m2 cho từng đường/phố trong thành phố đã chọn và sắp xếp giảm dần
        # df_median3 = df_selected_city_streets.groupby(['City', 'Street'])['price_value_trieu'].median().reset_index()
        # df_median3 = df_median3.sort_values(by='price_value_trieu', ascending=False)
        # # Tạo biểu đồ dựa trên DataFrame đã lọc và đã sắp xếp
        # fig = px.bar(df_median3, x='Street', y='price_value_trieu', title=f"Biểu đồ giá/m2 theo Đường - TP {selected_city}")
        # fig.update_layout(xaxis_title='Đường/Phố', yaxis_title='Trung vị giá / m2', xaxis_tickangle=-45, width=1200, height=700)
        # st.plotly_chart(fig)
        
if __name__ == '__main__':
    predictor = RealEstatePredictor()
    predictor.run()
