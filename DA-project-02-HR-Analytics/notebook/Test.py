import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ตั้งค่าสไตล์ของกราฟให้ดูคลีน เหมาะกับลง Notion
sns.set_theme(style="whitegrid")

# 1. โหลดข้อมูล (เปลี่ยนชื่อไฟล์ตามที่คุณเซฟไว้)
df = pd.read_csv('D:\DA-project-02-HR Analytics\DA-project-02-HR-Analytics\data\WA_Fn-UseC_-HR-Employee-Attrition.csv')

# ---------------------------------------------------------
# STEP 1: นิยาม "คนเก่ง" (Define Top Talent)
# ใน Dataset นี้ PerformanceRating จะมีแค่ 3 (Excellent) กับ 4 (Outstanding)
# เราจะสร้าง DataFrame ใหม่ที่คัดมาเฉพาะคนที่ได้ Rating 4 
# หรือคนที่ได้เงินเดือนขึ้นเยอะๆ (เช่น มากกว่าหรือเท่ากับ 15%)
# ---------------------------------------------------------
top_talent_df = df[(df['PerformanceRating'] == 4) | (df['PercentSalaryHike'] >= 15)]

print(f"จำนวนพนักงานทั้งหมด: {len(df)} คน")
print(f"จำนวน Top Talent: {len(top_talent_df)} คน\n")

# ---------------------------------------------------------
# STEP 2: หาอัตราการลาออกของกลุ่ม Top Talent
# ---------------------------------------------------------
# เทียบสัดส่วน Attrition ของคนเก่ง
attrition_rates = top_talent_df['Attrition'].value_counts(normalize=True) * 100
print("--- อัตราการลาออกของกลุ่ม Top Talent ---")
print(attrition_rates)
print("\n")

# ---------------------------------------------------------
# STEP 3: เจาะลึกสาเหตุ (Why do Top Talents leave?)
# แยกกลุ่มคนเก่งที่ "ลาออก" vs "ยังอยู่"
# ---------------------------------------------------------
# สร้างคอลัมน์ใหม่สำหรับ Attrition แบบตัวเลขเพื่อหาค่าเฉลี่ยได้ง่ายขึ้น (Yes = 1, No = 0)
top_talent_df = top_talent_df.copy()
top_talent_df['Attrition_Num'] = top_talent_df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)

# 3.1 ภาวะหมดไฟ (Burnout & OverTime)
print("--- สัดส่วนการทำ OverTime ของคนเก่งที่ลาออก vs ยังอยู่ ---")
# ดูว่าคนเก่งที่ลาออก ส่วนใหญ่ทำโอทีหรือไม่
ot_attrition = pd.crosstab(top_talent_df['OverTime'], top_talent_df['Attrition'], normalize='index') * 100
print(ot_attrition)
print("\n")

# 3.2 ทางตันของการเติบโต (Career Stagnation)
print("--- ค่าเฉลี่ยปีที่ไม่ได้เลื่อนขั้น และ ปีที่อยู่กับหัวหน้าคนเดิม ---")
stagnation_metrics = top_talent_df.groupby('Attrition')[['YearsSinceLastPromotion', 'YearsWithCurrManager']].mean()
print(stagnation_metrics)
print("\n")

# 3.3 เรื่องเงิน (Monthly Income)
print("--- ค่าเฉลี่ยเงินเดือน (Monthly Income) ---")
income_metrics = top_talent_df.groupby('Attrition')['MonthlyIncome'].mean()
print(income_metrics)