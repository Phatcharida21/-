import pandas as pd
import streamlit as st
import re

#streamlit run app.py


# อ่านชุดข้อมูลจากไฟล์ CSV
df = pd.read_csv(r"C:\demo3\สถานที่ท่องเที่ยวในจังหวัดขอนแก่น1.csv")

st.title('TOURIST ATTRACTIONS🚩')

# แทนที่ค่า NaN ด้วย "ไม่มีการระบุ"
df.fillna("ไม่มีการระบุ", inplace=True)
# ให้รหัสไปรษณีย์เป็นสตริง
df['postalcode'] = df['postalcode'].astype(str)
# ตัดช่องว่างนำหน้าและต่อท้ายออกจากชื่อคอลัมน์
df.columns = df.columns.str.strip()

# สร้างตัวเลือกสำหรับ Category
category_options = df['Category'].unique()
selected_categories = st.multiselect('เลือกประเภทสถานที่ท่องเที่ยว', category_options)

# สร้างตัวเลือกสำหรับ Target Group
target_group_options = ['กลุ่มครอบครัว', 'กลุ่มวัยทำงาน', 'กลุ่มนักเรียนนักศึกษา', 'เยาวชน', 'วัยรุ่น', 'กลุ่มคู่รัก', 'คู่แต่งงาน', 'ทุกช่วงวัย']
selected_target_groups = st.multiselect('เลือกประเภทสถานที่ท่องเที่ยว', target_group_options)

# Input ของ budget
budget = st.number_input('ป้อนงบประมาณของคุณ', min_value=0.0, format='%f')

# Input age และตรวจสอบ age
age = st.number_input('ป้อนอายุ', min_value=0, max_value=150, value=0)
# เลือก ticket price ที่จะรวม โดยขึ้นอยู่กับอายุ
if age >= 18:
    ticket_price_column = 'ticketPrice ThaiAdult'
else:
    ticket_price_column = 'ticketPrice ThaiChild'

# กรองข้อมูลตาม Category และ Target Group
filtered_df = df[df['Category'].isin(selected_categories) & df['Target Group'].apply(lambda x: any(target in x for target in selected_target_groups))]

# แสดงข้อมูลที่กรอง
# ใช้ st.container() ร่วมกับการกำหนดสไตล์ CSS
for index, row in filtered_df.iterrows():
    # ใช้ st.container() เพื่อสร้างบล็อกที่สามารถกำหนดสไตล์ได้
    with st.container():
        # กำหนดสไตล์ CSS ด้วย st.markdown() และใช้ unsafe_allow_html=True เพื่อให้ HTML ทำงาน
        st.markdown(f"""
            <style>
            .block{index} {{
                border: 2px solid #4CAF50;  /* กำหนดสีขอบ */
                border-radius: 10px;  /* กำหนดรูปแบบขอบให้มน */
                padding: 10px;  /* กำหนดระยะห่างภายใน */
                margin: 10px 0;  /* กำหนดระยะห่างภายนอก */
            }}
            </style>
            <div class="block{index}">
                <h4>{row['Name']}</h4>
                <p>ประเภท: {row["Category"]}</p>
                <p>{row["detail"]}</p>
                <p>ที่อยู่: {row["province"]} {row["district"]} {row["subdistrict"]} {row["postalcode"]}</p>
                <p>ค่าเข้าชม: {row[ticket_price_column]}</p>
                <p>เหมาะสำหรับ: {row["Target Group"]}</p>
                <p>การขนส่ง: {row["transportation"]}</p>
                <p>สิ่งอำนวยความสะดวก: {row["facility"]}</p>
                <p>ติดต่อ: {row["telephone"]}</p>
                <p>eMail: {row["eMail"]}</p>
                <p>Website: {row["Website"]}</p>
                <p>ช่วงเวลาเปิดทำการ: {row["businessHour"]}</p>
            </div>
        """, unsafe_allow_html=True)

# คำนวณผลรวมของราคาตั๋ว
total_ticket_price = filtered_df[ticket_price_column].sum()
# แสดงงบประมาณของผู้ใช้
st.write(f'งบประมาณของคุณ: {budget}')
# แสดงผลรวมของราคาตั๋ว
st.write(f'ผลรวมค่าเข้าชมทั้งหมด: {total_ticket_price}')
# เช็คว่าค่าใช้จ่ายเกินงบประมาณหรือไม่และแสดงข้อความ
if total_ticket_price > budget:
    st.error('ค่าใช้จ่ายเกินงบประมาณของคุณ')
else:
    st.success('ค่าใช้จ่ายยังไม่เกินงบประมาณของคุณ')
