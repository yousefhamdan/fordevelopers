import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import sqlalchemy
from pymysql.err import DataError
from datetime import datetime
import re

# Create an SQLAlchemy engine for the "investmentdb4" schema
engine = create_engine("mysql+pymysql://hamdan:itc-web-M1@109.237.202.133:3306/investmentdb6")


# Define a function to read data from a specific table in the database
def read_data_from_db(table_name):
    # try:
    sql = f"SELECT * FROM {table_name};"
    df = pd.read_sql(sql, engine)
    # except:
    #     err = f"الرجاء الحار بالانظار قليلا وشكرا."
    #     st.error(err)
    #     pass
    return df


# Define a function to update data in a specific table
def update_data_in_db(data, table_name):
    expected_dtypes={
    'الدولة':sqlalchemy.types.VARCHAR(200),
    'العاصمة':sqlalchemy.types.VARCHAR(200),
    'العملة':sqlalchemy.types.VARCHAR(200),
    'اللغة_الرسمية':sqlalchemy.types.VARCHAR(200),
    'عدد_السكان':sqlalchemy.types.INTEGER,
    'عدد_السكان_Source':sqlalchemy.types.TEXT,
    'عدد_السكان_Logic':sqlalchemy.types.TEXT,
    'عدد_السكان_Comments':sqlalchemy.types.TEXT,
    'نسبة_النمو_السكاني%':sqlalchemy.types.Float,
    'نسبة_النمو_السكاني%_Source':sqlalchemy.types.TEXT,
    'نسبة_النمو_السكاني%_Logic':sqlalchemy.types.TEXT,
    'نسبة_النمو_السكاني%_Comments':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_ذكر':sqlalchemy.types.Float,
    'متوسط_عمر_السكان_ذكر_Source':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_ذكر_Logic':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_ذكر_Comments':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_أنثى':sqlalchemy.types.Float,
    'متوسط_عمر_السكان_أنثى_Source':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_أنثى_Logic':sqlalchemy.types.TEXT,
    'متوسط_عمر_السكان_أنثى_Comments':sqlalchemy.types.TEXT,
    'نسبة_البطالة%':sqlalchemy.types.Float,
    'نسبة_البطالة%_Source':sqlalchemy.types.TEXT,
    'نسبة_البطالة%_Logic':sqlalchemy.types.TEXT,
    'نسبة_البطالة%_Comments':sqlalchemy.types.TEXT,
    'الحد_الأدنى_للأجور_شهري_بالدولار':sqlalchemy.types.Float,
    'الحد_الأدنى_للأجور_شهري_بالدولار_Source':sqlalchemy.types.TEXT,
    'الحد_الأدنى_للأجور_شهري_بالدولار_Logic':sqlalchemy.types.TEXT,
    'الحد_الأدنى_للأجور_شهري_بالدولار_Comments':sqlalchemy.types.TEXT,
    'نسبة_السكان_تحت_خط_الفقر_المحلي%':sqlalchemy.types.Float,
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Source':sqlalchemy.types.TEXT,
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Logic':sqlalchemy.types.TEXT,
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Comments':sqlalchemy.types.TEXT,
    'متوسط_الدخل_للاسرة_سنوي_بالدولار':sqlalchemy.types.Float,
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Source':sqlalchemy.types.TEXT,
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Logic':sqlalchemy.types.TEXT,
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Comments':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الاجمالي_بالمليار_دولار':sqlalchemy.types.Float,
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار':sqlalchemy.types.Float,
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Source':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Logic':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Comments':sqlalchemy.types.TEXT,
    'متوسط_الدخل_الفردي_سنوي_بالدولار':sqlalchemy.types.Float,
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Source':sqlalchemy.types.TEXT,
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Logic':sqlalchemy.types.TEXT,
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Comments':sqlalchemy.types.TEXT,
    'سعر_صرف_العملة_مقابل_الدولار':sqlalchemy.types.Float,
    'سعر_صرف_العملة_مقابل_الدولار_Source':sqlalchemy.types.TEXT,
    'سعر_صرف_العملة_مقابل_الدولار_Logic':sqlalchemy.types.TEXT,
    'سعر_صرف_العملة_مقابل_الدولار_Comments':sqlalchemy.types.TEXT,
    'نسبة_النمو_بالناتج_المحلي%':sqlalchemy.types.Float,
    'نسبة_النمو_بالناتج_المحلي%_Source':sqlalchemy.types.TEXT,
    'نسبة_النمو_بالناتج_المحلي%_Logic':sqlalchemy.types.TEXT,
    'نسبة_النمو_بالناتج_المحلي%_Comments':sqlalchemy.types.TEXT,
    'الناتج_القومي_الاجمالي_بالمليار_دولار':sqlalchemy.types.Float,
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'حجم_الموازنة_العامة_للنفقات_بالمليار':sqlalchemy.types.Float,
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Source':sqlalchemy.types.TEXT,
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Logic':sqlalchemy.types.TEXT,
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Comments':sqlalchemy.types.TEXT,
    'GDP%_نسبة_الموازنة_العامة':sqlalchemy.types.Float,
    'GDP%_نسبة_الموازنة_العامة_Source':sqlalchemy.types.TEXT,
    'GDP%_نسبة_الموازنة_العامة_Logic':sqlalchemy.types.TEXT,
    'GDP%_نسبة_الموازنة_العامة_Comments':sqlalchemy.types.TEXT,
    'سنة_الموازنة_العامة':sqlalchemy.types.Float,
    'سنة_الموازنة_العامة_Source':sqlalchemy.types.TEXT,
    'سنة_الموازنة_العامة_Logic':sqlalchemy.types.TEXT,
    'سنة_الموازنة_العامة_Comments':sqlalchemy.types.TEXT,
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار':sqlalchemy.types.Float,
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Source':sqlalchemy.types.TEXT,
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Logic':sqlalchemy.types.TEXT,
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Comments':sqlalchemy.types.TEXT,
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار':sqlalchemy.types.Float,
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Source':sqlalchemy.types.TEXT,
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Logic':sqlalchemy.types.TEXT,
    'العجز_الكلي_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Comments':sqlalchemy.types.TEXT,
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%':sqlalchemy.types.Float,
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Source':sqlalchemy.types.TEXT,
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Logic':sqlalchemy.types.TEXT,
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Comments':sqlalchemy.types.TEXT,
    'نسبة_التضخم%':sqlalchemy.types.Float,
    'نسبة_التضخم%_Source':sqlalchemy.types.TEXT,
    'نسبة_التضخم%_Logic':sqlalchemy.types.TEXT,
    'نسبة_التضخم%_Comments':sqlalchemy.types.TEXT,
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%':sqlalchemy.types.Float,
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Source':sqlalchemy.types.TEXT,
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Logic':sqlalchemy.types.TEXT,
    'العجز_الكلي_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Comments':sqlalchemy.types.TEXT,
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%':sqlalchemy.types.Float,
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Source':sqlalchemy.types.TEXT,
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Logic':sqlalchemy.types.TEXT,
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Comments':sqlalchemy.types.TEXT,
    'عجز_ميزان_المدفوعات_بالمليون_دولار':sqlalchemy.types.Float,
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Source':sqlalchemy.types.TEXT,
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Logic':sqlalchemy.types.TEXT,
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Comments':sqlalchemy.types.TEXT,
    'الميزان_التجاري_بالمليار_دولار':sqlalchemy.types.Float,
    'الميزان_التجاري_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'الميزان_التجاري_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'الميزان_التجاري_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'قيمة_الواردات_بالمليار_دولار':sqlalchemy.types.Float,
    'قيمة_الواردات_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'قيمة_الواردات_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'قيمة_الواردات_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'قيمة_الصادرات_بالمليون_دولار':sqlalchemy.types.Float,
    'قيمة_الصادرات_بالمليون_دولار_Source':sqlalchemy.types.TEXT,
    'قيمة_الصادرات_بالمليون_دولار_Logic':sqlalchemy.types.TEXT,
    'قيمة_الصادرات_بالمليون_دولار_Comments':sqlalchemy.types.TEXT,
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%':sqlalchemy.types.Float,
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Source':sqlalchemy.types.TEXT,
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Logic':sqlalchemy.types.TEXT,
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Comments':sqlalchemy.types.TEXT,
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار':sqlalchemy.types.Float,
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Source':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Logic':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Comments':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Source':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Logic':sqlalchemy.types.TEXT,
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Comments':sqlalchemy.types.TEXT,
    'احتياطات_النقد_الأجنبي_بالمليار_دولار':sqlalchemy.types.Float,
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_على_الودائع%':sqlalchemy.types.Float,
    'نسبة_الفائدة_على_الودائع%_Source':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_على_الودائع%_Logic':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_على_الودائع%_Comments':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_على_التسهيلات_الإئتمانية_للبنوك_المرخصة/كمبيالات%':sqlalchemy.types.Float,
    'نسبة_الفائدة_لتسهيلات_الإئتمانية_للبنوك/كمبيالات%_Source':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/كمبيالات%_Logic':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/كمبيالات%_Comments':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_على_التسهيلات_الإئتمانية_للبنوك_المرخصة/جاري-مدين%':sqlalchemy.types.Float,
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Source':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Logic':sqlalchemy.types.TEXT,
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Comments':sqlalchemy.types.TEXT,
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار':sqlalchemy.types.Float,
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Source':sqlalchemy.types.TEXT,
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Logic':sqlalchemy.types.TEXT,
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Comments':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_المبيعات%':sqlalchemy.types.Float,
    'نسبة_ضريبة_المبيعات%_Source':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_المبيعات%_Logic':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_المبيعات%_Comments':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الفرد%':sqlalchemy.types.Float,
    'نسبة_ضريبة_الدخل_على_الفرد%_Source':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الفرد%_Logic':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الفرد%_Comments':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الشركات%':sqlalchemy.types.Float,
    'نسبة_ضريبة_الدخل_على_الشركات%_Source':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الشركات%_Logic':sqlalchemy.types.TEXT,
    'نسبة_ضريبة_الدخل_على_الشركات%_Comments':sqlalchemy.types.TEXT,
    'ضريبة_الأرباح%':sqlalchemy.types.Float,
    'ضريبة_الأرباح%_Source':sqlalchemy.types.TEXT,
    'ضريبة_الأرباح%_Logic':sqlalchemy.types.TEXT,
    'ضريبة_الأرباح%_Comments':sqlalchemy.types.TEXT,
    'ضريبة_الارباح_قطاع_البنوك%':sqlalchemy.types.Float,
    'ضريبة_الارباح_قطاع_البنوك%_Source':sqlalchemy.types.TEXT,
    'ضريبة_الارباح_قطاع_البنوك%_Logic':sqlalchemy.types.TEXT,
    'ضريبة_الارباح_قطاع_البنوك%_Comments':sqlalchemy.types.TEXT,
    'مؤشر_الفساد':sqlalchemy.types.Float,
    'مؤشر_الفساد_Source':sqlalchemy.types.TEXT,
    'مؤشر_الفساد_Logic':sqlalchemy.types.TEXT,
    'مؤشر_الفساد_Comments':sqlalchemy.types.TEXT,
    'الترتيب_العالمي_على_مؤشر_الفساد':sqlalchemy.types.Float,
    'الترتيب_العالمي_على_مؤشر_الفساد_Source':sqlalchemy.types.TEXT,
    'الترتيب_العالمي_على_مؤشر_الفساد_Logic':sqlalchemy.types.TEXT,
    'الترتيب_العالمي_على_مؤشر_الفساد_Comments':sqlalchemy.types.TEXT,
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال':sqlalchemy.types.Float,
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Source':sqlalchemy.types.TEXT,
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Logic':sqlalchemy.types.TEXT,
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Comments':sqlalchemy.types.TEXT,
    'كثافة_مؤسسات_الأعمال_الجديدة':sqlalchemy.types.Float,
    'كثافة_مؤسسات_الأعمال_الجديدة_Source':sqlalchemy.types.TEXT,
    'كثافة_مؤسسات_الأعمال_الجديدة_Logic':sqlalchemy.types.TEXT,
    'كثافة_مؤسسات_الأعمال_الجديدة_Comments':sqlalchemy.types.TEXT,
    'S&P_التصنيف_الائتماني_حسب_مؤشر':sqlalchemy.types.VARCHAR(200),
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Source':sqlalchemy.types.TEXT,
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Logic':sqlalchemy.types.TEXT,
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Comments':sqlalchemy.types.TEXT,
    "Moody's_التصنيف_الائتماني_حسب_مؤشر":sqlalchemy.types.VARCHAR(200),
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Source":sqlalchemy.types.TEXT,
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Logic":sqlalchemy.types.TEXT,
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Comments":sqlalchemy.types.TEXT,
    'Fitch_التصنيف_الائتماني_حسب_مؤشر':sqlalchemy.types.VARCHAR(200),
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Source':sqlalchemy.types.TEXT,
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Logic':sqlalchemy.types.TEXT,
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Comments':sqlalchemy.types.TEXT,
    'أبرز_الصادرات':sqlalchemy.types.TEXT,
    'أبرز_الصادرات_Source':sqlalchemy.types.TEXT,
    'أبرز_الصادرات_Logic':sqlalchemy.types.TEXT,
    'أبرز_الصادرات_Comments':sqlalchemy.types.TEXT,
    'أبرز_الواردات':sqlalchemy.types.TEXT,
    'أبرز_الواردات_Source':sqlalchemy.types.TEXT,
    'أبرز_الواردات_Logic':sqlalchemy.types.TEXT,
    'أبرز_الواردات_Comments':sqlalchemy.types.TEXT,
    'السنة':sqlalchemy.types.INTEGER,
    'الناتج_المحلي_الإجمالي_مليار$_Actual':sqlalchemy.types.Float,
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Source':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Formula':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Logic':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Comments':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Weight':sqlalchemy.types.Float,
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Formula':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Logic':sqlalchemy.types.TEXT,
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Comments':sqlalchemy.types.TEXT,
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual':sqlalchemy.types.Float,
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Source':sqlalchemy.types.TEXT,
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Formula':sqlalchemy.types.TEXT,
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Logic':sqlalchemy.types.TEXT,
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Comments':sqlalchemy.types.TEXT,
    'النمو_في_الناتج_المحلي_الإجمالي_Weight':sqlalchemy.types.Float,
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Formula':sqlalchemy.types.TEXT,
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Logic':sqlalchemy.types.TEXT,
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Comments':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي%_Actual':sqlalchemy.types.Float,
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Source':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Formula':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Logic':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Comments':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي_Weight':sqlalchemy.types.Float,
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Formula':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Logic':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الاستثمار%_Actual':sqlalchemy.types.Float,
    'نمو_الاستثمار%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الاستثمار%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الاستثمار%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الاستثمار%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight':sqlalchemy.types.Float,
    'نمو_الاستثمار_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight_Comments':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي%_Actual':sqlalchemy.types.Float,
    'النمو_في_الإنفاق_الحكومي%_Actual_Source':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي%_Actual_Formula':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي%_Actual_Logic':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي%_Actual_Comments':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي_Weight':sqlalchemy.types.Float,
    'النمو_في_الإنفاق_الحكومي_Weight_Formula':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي_Weight_Logic':sqlalchemy.types.TEXT,
    'النمو_في_الإنفاق_الحكومي_Weight_Comments':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي%_Actual':sqlalchemy.types.Float,
    'العجز_المالي_الحكومي%_Actual_Source':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي%_Actual_Formula':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي%_Actual_Logic':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي%_Actual_Comments':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي_Weight':sqlalchemy.types.Float,
    'العجز_المالي_الحكومي_Weight_Formula':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي_Weight_Logic':sqlalchemy.types.TEXT,
    'العجز_المالي_الحكومي_Weight_Comments':sqlalchemy.types.TEXT,
    'GDP%_الدين_الحكومي_Actual':sqlalchemy.types.Float,
    'GDP%_الدين_الحكومي_Actual_Source':sqlalchemy.types.TEXT,
    'GDP%_الدين_الحكومي_Actual_Formula':sqlalchemy.types.TEXT,
    'GDP%_الدين_الحكومي_Actual_Logic':sqlalchemy.types.TEXT,
    'GDP%_الدين_الحكومي_Actual_Comments':sqlalchemy.types.TEXT,
    'الدين_الحكومي_Weight':sqlalchemy.types.Float,
    'الدين_الحكومي_Weight_Formula':sqlalchemy.types.TEXT,
    'الدين_الحكومي_Weight_Logic':sqlalchemy.types.TEXT,
    'الدين_الحكومي_Weight_Comments':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Actual':sqlalchemy.types.Float,
    'النمو_في_القوة_العمالية_Actual_Source':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Actual_Formula':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Actual_Logic':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Actual_Comments':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Weight':sqlalchemy.types.Float,
    'النمو_في_القوة_العمالية_Weight_Formula':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Weight_Logic':sqlalchemy.types.TEXT,
    'النمو_في_القوة_العمالية_Weight_Comments':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص%_Actual':sqlalchemy.types.Float,
    'دين_القطاع_الخاص%_Actual_Source':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص%_Actual_Formula':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص%_Actual_Logic':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص%_Actual_Comments':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص_Weight':sqlalchemy.types.Float,
    'دين_القطاع_الخاص_Weight_Formula':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص_Weight_Logic':sqlalchemy.types.TEXT,
    'دين_القطاع_الخاص_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual':sqlalchemy.types.Float,
    'نمو_الصادرات%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الصادرات_Weight':sqlalchemy.types.Float,
    'نمو_الصادرات_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الصادرات_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الصادرات_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual':sqlalchemy.types.Float,
    'نمو_الواردات%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الواردات_Weight':sqlalchemy.types.Float,
    'نمو_الواردات_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الواردات_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الواردات_Weight_Comments':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual':sqlalchemy.types.VARCHAR(200),
    'الاستقرار_النقدي_Actual_Source':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Formula':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Logic':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Comments':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight':sqlalchemy.types.Float,
    'الاستقرار_النقدي_Weight_Formula':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight_Logic':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight_Comments':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال%_Actual':sqlalchemy.types.Float,
    'إجمالي_تكوين_رأس_المال%_Actual_Source':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال%_Actual_Formula':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال%_Actual_Logic':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال%_Actual_Comments':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال_Weight':sqlalchemy.types.Float,
    'إجمالي_تكوين_رأس_المال_Weight_Formula':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال_Weight_Logic':sqlalchemy.types.TEXT,
    'إجمالي_تكوين_رأس_المال_Weight_Comments':sqlalchemy.types.TEXT,
    'GDP%_صافي_الاستثمار_الأجنبي_Actual':sqlalchemy.types.Float,
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Source':sqlalchemy.types.TEXT,
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Formula':sqlalchemy.types.TEXT,
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Logic':sqlalchemy.types.TEXT,
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Comments':sqlalchemy.types.TEXT,
    'صافي_الاستثمار_الأجنبي_Weight':sqlalchemy.types.Float,
    'صافي_الاستثمار_الأجنبي_Weight_Formula':sqlalchemy.types.TEXT,
    'صافي_الاستثمار_الأجنبي_Weight_Logic':sqlalchemy.types.TEXT,
    'صافي_الاستثمار_الأجنبي_Weight_Comments':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية%_Actual':sqlalchemy.types.Float,
    'تعزيز_الانتاجية%_Actual_Source':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية%_Actual_Formula':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية%_Actual_Logic':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية%_Actual_Comments':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية_Weight':sqlalchemy.types.Float,
    'تعزيز_الانتاجية_Weight_Formula':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية_Weight_Logic':sqlalchemy.types.TEXT,
    'تعزيز_الانتاجية_Weight_Comments':sqlalchemy.types.TEXT,
    'المجموع':sqlalchemy.types.Float,
    'المجموع_Formula':sqlalchemy.types.TEXT,
    'المجموع_Logic':sqlalchemy.types.TEXT,
    'المجموع_Comments':sqlalchemy.types.TEXT,
    'إيرادات_الناتج_المحلي_الإجمالي':sqlalchemy.types.TEXT,
    'إيرادات_الناتج_المحلي_الإجمالي_Sources':sqlalchemy.types.TEXT,
    'إيرادات_الناتج_المحلي_الإجمالي_Logic':sqlalchemy.types.TEXT,
    'إيرادات_الناتج_المحلي_الإجمالي_Comments':sqlalchemy.types.TEXT,
    'إيرادات_الموازنة_العامة':sqlalchemy.types.TEXT,
    'إيرادات_الموازنة_العامة_Sources':sqlalchemy.types.TEXT,
    'إيرادات_الموازنة_العامة_Logic':sqlalchemy.types.TEXT,
    'إيرادات_الموازنة_العامة_Comments':sqlalchemy.types.TEXT,
    'نفقات_الموازنة_العامة':sqlalchemy.types.TEXT,
    'نفقات_الموازنة_العامة_Sources':sqlalchemy.types.TEXT,
    'نفقات_الموازنة_العامة_Logic':sqlalchemy.types.TEXT,
    'نفقات_الموازنة_العامة_Comments':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Actual':sqlalchemy.types.Float,
    '(GDP%)_الاستثمار_Actual_Source':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Actual_Formula':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Actual_Logic':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Actual_Comments':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Weight':sqlalchemy.types.Float,
    '(GDP%)_الاستثمار_Weight_Formula':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Weight_Logic':sqlalchemy.types.TEXT,
    '(GDP%)_الاستثمار_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Actual':sqlalchemy.types.Float,
    'نمو_الاستثمار_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight':sqlalchemy.types.Float,
    'نمو_الاستثمار_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الاستثمار_Weight_Comments':sqlalchemy.types.TEXT,
    '%الابتكار_في_الاقتصاد_Actual':sqlalchemy.types.Float,
    '%الابتكار_في_الاقتصاد_Actual_Source':sqlalchemy.types.TEXT,
    '%الابتكار_في_الاقتصاد_Actual_Formula':sqlalchemy.types.TEXT,
    '%الابتكار_في_الاقتصاد_Actual_Logic':sqlalchemy.types.TEXT,
    '%الابتكار_في_الاقتصاد_Actual_Comments':sqlalchemy.types.TEXT,
    'الابتكار_في_الاقتصاد_Weight':sqlalchemy.types.Float,
    'الابتكار_في_الاقتصاد_Weight_Formula':sqlalchemy.types.TEXT,
    'الابتكار_في_الاقتصاد_Weight_Logic':sqlalchemy.types.TEXT,
    'الابتكار_في_الاقتصاد_Weight_Comments':sqlalchemy.types.TEXT,
    '%الفائدة_على_الإقراض_Actual':sqlalchemy.types.Float,
    '%الفائدة_على_الإقراض_Actual_Source':sqlalchemy.types.TEXT,
    '%الفائدة_على_الإقراض_Actual_Formula':sqlalchemy.types.TEXT,
    '%الفائدة_على_الإقراض_Actual_Logic':sqlalchemy.types.TEXT,
    '%الفائدة_على_الإقراض_Actual_Comments':sqlalchemy.types.TEXT,
    'الفائدة_على_الإقراض_Weight':sqlalchemy.types.Float,
    'الفائدة_على_الإقراض_Weight_Formula':sqlalchemy.types.TEXT,
    'الفائدة_على_الإقراض_Weight_Logic':sqlalchemy.types.TEXT,
    'الفائدة_على_الإقراض_Weight_Comments':sqlalchemy.types.TEXT,
    'النمو_السكاني%_Actual':sqlalchemy.types.Float,
    'النمو_السكاني%_Actual_Source':sqlalchemy.types.TEXT,
    'النمو_السكاني%_Actual_Formula':sqlalchemy.types.TEXT,
    'النمو_السكاني%_Actual_Logic':sqlalchemy.types.TEXT,
    'النمو_السكاني%_Actual_Comments':sqlalchemy.types.TEXT,
    'النمو_السكاني_Weight':sqlalchemy.types.Float,
    'النمو_السكاني_Weight_Formula':sqlalchemy.types.TEXT,
    'النمو_السكاني_Weight_Logic':sqlalchemy.types.TEXT,
    'النمو_السكاني_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية%_Actual':sqlalchemy.types.Float,
    'نمو_القوة_العمالية%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية_Weight':sqlalchemy.types.Float,
    'نمو_القوة_العمالية_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_القوة_العمالية_Weight_Comments':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع%_Actual':sqlalchemy.types.Float,
    'الفائدة_على_الودائع%_Actual_Source':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع%_Actual_Formula':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع%_Actual_Logic':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع%_Actual_Comments':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع_Weight':sqlalchemy.types.Float,
    'الفائدة_على_الودائع_Weight_Formula':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع_Weight_Logic':sqlalchemy.types.TEXT,
    'الفائدة_على_الودائع_Weight_Comments':sqlalchemy.types.TEXT,
    'التضخم_Actual':sqlalchemy.types.Float,
    'التضخم_Actual_Source':sqlalchemy.types.TEXT,
    'التضخم_Actual_Formula':sqlalchemy.types.TEXT,
    'التضخم_Actual_Logic':sqlalchemy.types.TEXT,
    'التضخم_Actual_Comments':sqlalchemy.types.TEXT,
    'التضخم_Weight':sqlalchemy.types.Float,
    'التضخم_Weight_Formula':sqlalchemy.types.TEXT,
    'التضخم_Weight_Logic':sqlalchemy.types.TEXT,
    'التضخم_Weight_Comments':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual':sqlalchemy.types.VARCHAR(200),
    'الاستقرار_النقدي_Actual_Source':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Formula':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Logic':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Actual_Comments':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight':sqlalchemy.types.Float,
    'الاستقرار_النقدي_Weight_Formula':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight_Logic':sqlalchemy.types.TEXT,
    'الاستقرار_النقدي_Weight_Comments':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Actual':sqlalchemy.types.VARCHAR(200),
    'استقلالية_البنك_المركزي_Actual_Source':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Actual_Formula':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Actual_Logic':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Actual_Comments':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Weight':sqlalchemy.types.Float,
    'استقلالية_البنك_المركزي_Weight_Formula':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Weight_Logic':sqlalchemy.types.TEXT,
    'استقلالية_البنك_المركزي_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual':sqlalchemy.types.Float,
    'نمو_الصادرات%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Weight':sqlalchemy.types.Float,
    'نمو_الصادرات%_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الصادرات%_Weight_Comments':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual':sqlalchemy.types.Float,
    'نمو_الواردات%_Actual_Source':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Formula':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Logic':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Actual_Comments':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Weight':sqlalchemy.types.Float,
    'نمو_الواردات%_Weight_Formula':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Weight_Logic':sqlalchemy.types.TEXT,
    'نمو_الواردات%_Weight_Comments':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Actual':sqlalchemy.types.Float,
    'الميزان_التجاري_مليار$_Actual_Source':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Actual_Formula':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Actual_Logic':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Actual_Comments':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Weight':sqlalchemy.types.Float,
    'الميزان_التجاري_مليار$_Weight_Formula':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Weight_Logic':sqlalchemy.types.TEXT,
    'الميزان_التجاري_مليار$_Weight_Comments':sqlalchemy.types.TEXT,
    'العجز_النقدي%_Actual':sqlalchemy.types.Float,
    'العجز_النقدي%_Actual_Source':sqlalchemy.types.TEXT,
    'العجز_النقدي%_Actual_Formula':sqlalchemy.types.TEXT,
    'العجز_النقدي%_Actual_Logic':sqlalchemy.types.TEXT,
    'العجز_النقدي%_Actual_Comments':sqlalchemy.types.TEXT,
    'العجز_النقدي_Weight':sqlalchemy.types.Float,
    'العجز_النقدي_Weight_Formula':sqlalchemy.types.TEXT,
    'العجز_النقدي_Weight_Logic':sqlalchemy.types.TEXT,
    'العجز_النقدي_Weight_Comments':sqlalchemy.types.TEXT,
    '(GDP%)_الدين_الخارجي_Actual':sqlalchemy.types.Float,
    '(GDP%)_الدين_الخارجي_Actual_Source':sqlalchemy.types.TEXT,
    '(GDP%)_الدين_الخارجي_Actual_Formula':sqlalchemy.types.TEXT,
    '(GDP%)_الدين_الخارجي_Actual_Logic':sqlalchemy.types.TEXT,
    '(GDP%)_الدين_الخارجي_Actual_Comments':sqlalchemy.types.TEXT,
    'الدين_الخارجي_Weight':sqlalchemy.types.Float,
    'الدين_الخارجي_Weight_Formula':sqlalchemy.types.TEXT,
    'الدين_الخارجي_Weight_Logic':sqlalchemy.types.TEXT,
    'الدين_الخارجي_Weight_Comments':sqlalchemy.types.TEXT,
    'القطاع':sqlalchemy.types.VARCHAR(200),
    'القطاع_الفرعي':sqlalchemy.types.VARCHAR(200),
    'العنوان':sqlalchemy.types.TEXT,
    'الوصف':sqlalchemy.types.TEXT,
    'التكلفة_التقريبية':sqlalchemy.types.TEXT,
    'العائد_على_الاستثمار':sqlalchemy.types.TEXT,
    '%استقرار_الاقتصاد_الكلي_Actual':sqlalchemy.types.Float,
    '%استقرار_الاقتصاد_الكلي_Actual_Source':sqlalchemy.types.TEXT,
    '%استقرار_الاقتصاد_الكلي_Actual_Formula':sqlalchemy.types.TEXT,
    '%استقرار_الاقتصاد_الكلي_Actual_Logic':sqlalchemy.types.TEXT,
    '%استقرار_الاقتصاد_الكلي_Actual_Comments':sqlalchemy.types.TEXT,
    'استقرار_الاقتصاد_الكلي_Weight':sqlalchemy.types.Float,
    'استقرار_الاقتصاد_الكلي_Weight_Formula':sqlalchemy.types.TEXT,
    'استقرار_الاقتصاد_الكلي_Weight_Logic':sqlalchemy.types.TEXT,
    'استقرار_الاقتصاد_الكلي_Weight_Comments':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات%_Actual':sqlalchemy.types.Float,
    'عدم_اليقين_في_السياسات%_Actual_Source':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات%_Actual_Formula':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات%_Actual_Logic':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات%_Actual_Comments':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات_Weight':sqlalchemy.types.Float,
    'عدم_اليقين_في_السياسات_Weight_Formula':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات_Weight_Logic':sqlalchemy.types.TEXT,
    'عدم_اليقين_في_السياسات_Weight_Comments':sqlalchemy.types.TEXT,
    'الفساد%_Actual':sqlalchemy.types.Float,
    'الفساد%_Actual_Source':sqlalchemy.types.TEXT,
    'الفساد%_Actual_Formula':sqlalchemy.types.TEXT,
    'الفساد%_Actual_Logic':sqlalchemy.types.TEXT,
    'الفساد%_Actual_Comments':sqlalchemy.types.TEXT,
    'الفساد_Weight':sqlalchemy.types.Float,
    'الفساد_Weight_Formula':sqlalchemy.types.TEXT,
    'الفساد_Weight_Logic':sqlalchemy.types.TEXT,
    'الفساد_Weight_Comments':sqlalchemy.types.TEXT,
    'معدل_الضرائب%_Actual':sqlalchemy.types.Float,
    'معدل_الضرائب%_Actual_Source':sqlalchemy.types.TEXT,
    'معدل_الضرائب%_Actual_Formula':sqlalchemy.types.TEXT,
    'معدل_الضرائب%_Actual_Logic':sqlalchemy.types.TEXT,
    'معدل_الضرائب%_Actual_Comments':sqlalchemy.types.TEXT,
    'معدل_الضرائب_Weight':sqlalchemy.types.Float,
    'معدل_الضرائب_Weight_Formula':sqlalchemy.types.TEXT,
    'معدل_الضرائب_Weight_Logic':sqlalchemy.types.TEXT,
    'معدل_الضرائب_Weight_Comments':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل%_Actual':sqlalchemy.types.Float,
    'التكلفة_والحصول_على_التمويل%_Actual_Source':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل%_Actual_Formula':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل%_Actual_Logic':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل%_Actual_Comments':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل_Weight':sqlalchemy.types.Float,
    'التكلفة_والحصول_على_التمويل_Weight_Formula':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل_Weight_Logic':sqlalchemy.types.TEXT,
    'التكلفة_والحصول_على_التمويل_Weight_Comments':sqlalchemy.types.TEXT,
    'الجريمة%_Actual':sqlalchemy.types.Float,
    'الجريمة%_Actual_Source':sqlalchemy.types.TEXT,
    'الجريمة%_Actual_Formula':sqlalchemy.types.TEXT,
    'الجريمة%_Actual_Logic':sqlalchemy.types.TEXT,
    'الجريمة%_Actual_Comments':sqlalchemy.types.TEXT,
    'الجريمة_Weight':sqlalchemy.types.Float,
    'الجريمة_Weight_Formula':sqlalchemy.types.TEXT,
    'الجريمة_Weight_Logic':sqlalchemy.types.TEXT,
    'الجريمة_Weight_Comments':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب%_Actual':sqlalchemy.types.Float,
    'اللوائح_وإدارة_الضرائب%_Actual_Source':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب%_Actual_Formula':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب%_Actual_Logic':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب%_Actual_Comments':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب_Weight':sqlalchemy.types.Float,
    'اللوائح_وإدارة_الضرائب_Weight_Formula':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب_Weight_Logic':sqlalchemy.types.TEXT,
    'اللوائح_وإدارة_الضرائب_Weight_Comments':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Actual':sqlalchemy.types.Float,
    'المهارات_الأساسية_في_الاقتصاد_Actual_Source':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Actual_Formula':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Actual_Logic':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Actual_Comments':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Weight':sqlalchemy.types.Float,
    'المهارات_الأساسية_في_الاقتصاد_Weight_Formula':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Weight_Logic':sqlalchemy.types.TEXT,
    'المهارات_الأساسية_في_الاقتصاد_Weight_Comments':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي%_Actual':sqlalchemy.types.Float,
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Source':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Formula':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Logic':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Comments':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي_Weight':sqlalchemy.types.Float,
    'جودة_التعليم_الابتدائي_والعالي_Weight_Formula':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي_Weight_Logic':sqlalchemy.types.TEXT,
    'جودة_التعليم_الابتدائي_والعالي_Weight_Comments':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية%_Actual':sqlalchemy.types.Float,
    'جودة_العناية_الصحية%_Actual_Source':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية%_Actual_Formula':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية%_Actual_Logic':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية%_Actual_Comments':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية_Weight':sqlalchemy.types.Float,
    'جودة_العناية_الصحية_Weight_Formula':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية_Weight_Logic':sqlalchemy.types.TEXT,
    'جودة_العناية_الصحية_Weight_Comments':sqlalchemy.types.TEXT,
    '%نظام_المحاكم_Actual':sqlalchemy.types.Float,
    '%نظام_المحاكم_Actual_Source':sqlalchemy.types.TEXT,
    '%نظام_المحاكم_Actual_Formula':sqlalchemy.types.TEXT,
    '%نظام_المحاكم_Actual_Logic':sqlalchemy.types.TEXT,
    '%نظام_المحاكم_Actual_Comments':sqlalchemy.types.TEXT,
    'نظام_المحاكم_Weight':sqlalchemy.types.Float,
    'نظام_المحاكم_Weight_Formula':sqlalchemy.types.TEXT,
    'نظام_المحاكم_Weight_Logic':sqlalchemy.types.TEXT,
    'نظام_المحاكم_Weight_Comments':sqlalchemy.types.TEXT,
    'النقل%_Actual':sqlalchemy.types.Float,
    'النقل%_Actual_Source':sqlalchemy.types.TEXT,
    'النقل%_Actual_Formula':sqlalchemy.types.TEXT,
    'النقل%_Actual_Logic':sqlalchemy.types.TEXT,
    'النقل%_Actual_Comments':sqlalchemy.types.TEXT,
    'النقل_Weight':sqlalchemy.types.Float,
    'النقل_Weight_Formula':sqlalchemy.types.TEXT,
    'النقل_Weight_Logic':sqlalchemy.types.TEXT,
    'النقل_Weight_Comments':sqlalchemy.types.TEXT,
    'الاتصالات%_Actual':sqlalchemy.types.Float,
    'الاتصالات%_Actual_Source':sqlalchemy.types.TEXT,
    'الاتصالات%_Actual_Formula':sqlalchemy.types.TEXT,
    'الاتصالات%_Actual_Logic':sqlalchemy.types.TEXT,
    'الاتصالات%_Actual_Comments':sqlalchemy.types.TEXT,
    'الاتصالات_Weight':sqlalchemy.types.Float,
    'الاتصالات_Weight_Formula':sqlalchemy.types.TEXT,
    'الاتصالات_Weight_Logic':sqlalchemy.types.TEXT,
    'الاتصالات_Weight_Comments':sqlalchemy.types.TEXT,
    'الرقمنة_Actual':sqlalchemy.types.Float,
    'الرقمنة_Actual_Source':sqlalchemy.types.TEXT,
    'الرقمنة_Actual_Formula':sqlalchemy.types.TEXT,
    'الرقمنة_Actual_Logic':sqlalchemy.types.TEXT,
    'الرقمنة_Actual_Comments':sqlalchemy.types.TEXT,
    'الرقمنة_Weight':sqlalchemy.types.Float,
    'الرقمنة_Weight_Formula':sqlalchemy.types.TEXT,
    'الرقمنة_Weight_Logic':sqlalchemy.types.TEXT,
    'الرقمنة_Weight_Comments':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة%_Actual':sqlalchemy.types.Float,
    'تكاليف_المعيشة%_Actual_Source':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة%_Actual_Formula':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة%_Actual_Logic':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة%_Actual_Comments':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة_Weight':sqlalchemy.types.Float,
    'تكاليف_المعيشة_Weight_Formula':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة_Weight_Logic':sqlalchemy.types.TEXT,
    'تكاليف_المعيشة_Weight_Comments':sqlalchemy.types.TEXT,
    'جودة_المعيشة%_Actual':sqlalchemy.types.Float,
    'جودة_المعيشة%_Actual_Source':sqlalchemy.types.TEXT,
    'جودة_المعيشة%_Actual_Formula':sqlalchemy.types.TEXT,
    'جودة_المعيشة%_Actual_Logic':sqlalchemy.types.TEXT,
    'جودة_المعيشة%_Actual_Comments':sqlalchemy.types.TEXT,
    'جودة_المعيشة_Weight':sqlalchemy.types.Float,
    'جودة_المعيشة_Weight_Formula':sqlalchemy.types.TEXT,
    'جودة_المعيشة_Weight_Logic':sqlalchemy.types.TEXT,
    'جودة_المعيشة_Weight_Comments':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Actual':sqlalchemy.types.Float,
    'GPI_السلام_العالمي_Actual_Source':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Actual_Formula':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Actual_Logic':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Actual_Comments':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Weight':sqlalchemy.types.Float,
    'GPI_السلام_العالمي_Weight_Formula':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Weight_Logic':sqlalchemy.types.TEXT,
    'GPI_السلام_العالمي_Weight_Comments':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Actual':sqlalchemy.types.Float,
    'PSI_الاستقرار_السياسي_العالمي_Actual_Source':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Actual_Formula':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Actual_Logic':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Actual_Comments':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Weight':sqlalchemy.types.Float,
    'PSI_الاستقرار_السياسي_العالمي_Weight_Formula':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Weight_Logic':sqlalchemy.types.TEXT,
    'PSI_الاستقرار_السياسي_العالمي_Weight_Comments':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Actual':sqlalchemy.types.Float,
    'CPI_مدركات_الفساد_Actual_Source':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Actual_Formula':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Actual_Logic':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Actual_Comments':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Weight':sqlalchemy.types.Float,
    'CPI_مدركات_الفساد_Weight_Formula':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Weight_Logic':sqlalchemy.types.TEXT,
    'CPI_مدركات_الفساد_Weight_Comments':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Actual':sqlalchemy.types.Float,
    'GTI_مكافحة_الإرهاب_Actual_Source':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Actual_Formula':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Actual_Logic':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Actual_Comments':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Weight':sqlalchemy.types.Float,
    'GTI_مكافحة_الإرهاب_Weight_Formula':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Weight_Logic':sqlalchemy.types.TEXT,
    'GTI_مكافحة_الإرهاب_Weight_Comments':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Actual':sqlalchemy.types.Float,
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Source':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Formula':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Logic':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Comments':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Weight':sqlalchemy.types.Float,
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Formula':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Logic':sqlalchemy.types.TEXT,
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Comments':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Actual':sqlalchemy.types.Float,
    'HDI_التنمية_البشرية_Actual_Source':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Actual_Formula':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Actual_Logic':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Actual_Comments':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Weight':sqlalchemy.types.Float,
    'HDI_التنمية_البشرية_Weight_Formula':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Weight_Logic':sqlalchemy.types.TEXT,
    'HDI_التنمية_البشرية_Weight_Comments':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Actual':sqlalchemy.types.Float,
    'TI_الشفافية_العالمي_Actual_Source':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Actual_Formula':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Actual_Logic':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Actual_Comments':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Weight':sqlalchemy.types.Float,
    'TI_الشفافية_العالمي_Weight_Formula':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Weight_Logic':sqlalchemy.types.TEXT,
    'TI_الشفافية_العالمي_Weight_Comments':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Actual':sqlalchemy.types.Float,
    'BEI_بيئة_الأعمال_Actual_Source':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Actual_Formula':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Actual_Logic':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Actual_Comments':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Weight':sqlalchemy.types.Float,
    'BEI_بيئة_الأعمال_Weight_Formula':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Weight_Logic':sqlalchemy.types.TEXT,
    'BEI_بيئة_الأعمال_Weight_Comments':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Actual':sqlalchemy.types.Float,
    'WJP_سيادة_القانون_Actual_Source':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Actual_Formula':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Actual_Logic':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Actual_Comments':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Weight':sqlalchemy.types.Float,
    'WJP_سيادة_القانون_Weight_Formula':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Weight_Logic':sqlalchemy.types.TEXT,
    'WJP_سيادة_القانون_Weight_Comments':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Actual':sqlalchemy.types.Float,
    'VAI_المشاركة_والمساءلة_Actual_Source':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Actual_Formula':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Actual_Logic':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Actual_Comments':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Weight':sqlalchemy.types.Float,
    'VAI_المشاركة_والمساءلة_Weight_Formula':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Weight_Logic':sqlalchemy.types.TEXT,
    'VAI_المشاركة_والمساءلة_Weight_Comments':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Actual':sqlalchemy.types.Float,
    'OCI_الجريمة_المنظمة_Actual_Source':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Actual_Formula':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Actual_Logic':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Actual_Comments':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Weight':sqlalchemy.types.Float,
    'OCI_الجريمة_المنظمة_Weight_Formula':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Weight_Logic':sqlalchemy.types.TEXT,
    'OCI_الجريمة_المنظمة_Weight_Comments':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual':sqlalchemy.types.Float,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Source':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Formula':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Logic':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Comments':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight':sqlalchemy.types.Float,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Formula':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Logic':sqlalchemy.types.TEXT,
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Comments':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual':sqlalchemy.types.Float,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Source':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Formula':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Logic':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Comments':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight':sqlalchemy.types.Float,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Formula':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Logic':sqlalchemy.types.TEXT,
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Comments':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Actual':sqlalchemy.types.Float,
    'DI_الديمقراطية_Actual_Source':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Actual_Formula':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Actual_Logic':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Actual_Comments':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Weight':sqlalchemy.types.Float,
    'DI_الديمقراطية_Weight_Formula':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Weight_Logic':sqlalchemy.types.TEXT,
    'DI_الديمقراطية_Weight_Comments':sqlalchemy.types.TEXT,
    'النتيجة':sqlalchemy.types.TEXT, 
    'التوصية':sqlalchemy.types.TEXT, 
    'فيديو':sqlalchemy.types.VARCHAR(3500),
    'القطاع_الرئيسي':sqlalchemy.types.VARCHAR(250), 
    'القطاع_الفرعي':sqlalchemy.types.VARCHAR(250), 
    'متاح':sqlalchemy.types.INTEGER}
    


    expected_data_types={
    'الدولة':'VARCHAR',
    'العاصمة':'VARCHAR',
    'العملة':'VARCHAR',
    'اللغة_الرسمية':'VARCHAR',
    'عدد_السكان':'INT',
    'عدد_السكان_Source':'VARCHAR',
    'عدد_السكان_Logic':'VARCHAR',
    'عدد_السكان_Comments':'VARCHAR',
    'نسبة_النمو_السكاني%':'FLOAT',
    'نسبة_النمو_السكاني%_Source':'VARCHAR',
    'نسبة_النمو_السكاني%_Logic':'VARCHAR',
    'نسبة_النمو_السكاني%_Comments':'VARCHAR',
    'متوسط_عمر_السكان_ذكر':'FLOAT',
    'متوسط_عمر_السكان_ذكر_Source':'VARCHAR',
    'متوسط_عمر_السكان_ذكر_Logic':'VARCHAR',
    'متوسط_عمر_السكان_ذكر_Comments':'VARCHAR',
    'متوسط_عمر_السكان_أنثى':'FLOAT',
    'متوسط_عمر_السكان_أنثى_Source':'VARCHAR',
    'متوسط_عمر_السكان_أنثى_Logic':'VARCHAR',
    'متوسط_عمر_السكان_أنثى_Comments':'VARCHAR',
    'نسبة_البطالة%':'FLOAT',
    'نسبة_البطالة%_Source':'VARCHAR',
    'نسبة_البطالة%_Logic':'VARCHAR',
    'نسبة_البطالة%_Comments':'VARCHAR',
    'الحد_الأدنى_للأجور_شهري_بالدولار':'FLOAT',
    'الحد_الأدنى_للأجور_شهري_بالدولار_Source':'VARCHAR',
    'الحد_الأدنى_للأجور_شهري_بالدولار_Logic':'VARCHAR',
    'الحد_الأدنى_للأجور_شهري_بالدولار_Comments':'VARCHAR',
    'نسبة_السكان_تحت_خط_الفقر_المحلي%':'FLOAT',
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Source':'VARCHAR',
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Logic':'VARCHAR',
    'نسبة_السكان_تحت_خط_الفقر_المحلي%_Comments':'VARCHAR',
    'متوسط_الدخل_للاسرة_سنوي_بالدولار':'FLOAT',
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Source':'VARCHAR',
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Logic':'VARCHAR',
    'متوسط_الدخل_للاسرة_سنوي_بالدولار_Comments':'VARCHAR',
    'الناتج_المحلي_الاجمالي_بالمليار_دولار':'FLOAT',
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Source':'VARCHAR',
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Logic':'VARCHAR',
    'الناتج_المحلي_الاجمالي_بالمليار_دولار_Comments':'VARCHAR',
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار':'FLOAT',
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Source':'VARCHAR',
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Logic':'VARCHAR',
    'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Comments':'VARCHAR',
    'متوسط_الدخل_الفردي_سنوي_بالدولار':'FLOAT',
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Source':'VARCHAR',
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Logic':'VARCHAR',
    'متوسط_الدخل_الفردي_سنوي_بالدولار_Comments':'VARCHAR',
    'سعر_صرف_العملة_مقابل_الدولار':'FLOAT',
    'سعر_صرف_العملة_مقابل_الدولار_Source':'VARCHAR',
    'سعر_صرف_العملة_مقابل_الدولار_Logic':'VARCHAR',
    'سعر_صرف_العملة_مقابل_الدولار_Comments':'VARCHAR',
    'نسبة_النمو_بالناتج_المحلي%':'FLOAT',
    'نسبة_النمو_بالناتج_المحلي%_Source':'VARCHAR',
    'نسبة_النمو_بالناتج_المحلي%_Logic':'VARCHAR',
    'نسبة_النمو_بالناتج_المحلي%_Comments':'VARCHAR',
    'الناتج_القومي_الاجمالي_بالمليار_دولار':'FLOAT',
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Source':'VARCHAR',
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Logic':'VARCHAR',
    'الناتج_القومي_الاجمالي_بالمليار_دولار_Comments':'VARCHAR',
    'حجم_الموازنة_العامة_للنفقات_بالمليار':'FLOAT',
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Source':'VARCHAR',
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Logic':'VARCHAR',
    'حجم_الموازنة_العامة_للنفقات_بالمليار_Comments':'VARCHAR',
    'GDP%_نسبة_الموازنة_العامة':'FLOAT',
    'GDP%_نسبة_الموازنة_العامة_Source':'VARCHAR',
    'GDP%_نسبة_الموازنة_العامة_Logic':'VARCHAR',
    'GDP%_نسبة_الموازنة_العامة_Comments':'VARCHAR',
    'سنة_الموازنة_العامة':'FLOAT',
    'سنة_الموازنة_العامة_Source':'VARCHAR',
    'سنة_الموازنة_العامة_Logic':'VARCHAR',
    'سنة_الموازنة_العامة_Comments':'VARCHAR',
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار':'FLOAT',
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Source':'VARCHAR',
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Logic':'VARCHAR',
    'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Comments':'VARCHAR',
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار':'FLOAT',
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Source':'VARCHAR',
    'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Logic':'VARCHAR',
    'العجز_الكلي_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Comments':'VARCHAR',
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%':'FLOAT',
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Source':'VARCHAR',
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Logic':'VARCHAR',
    'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Comments':'VARCHAR',
    'نسبة_التضخم%':'FLOAT',
    'نسبة_التضخم%_Source':'VARCHAR',
    'نسبة_التضخم%_Logic':'VARCHAR',
    'نسبة_التضخم%_Comments':'VARCHAR',
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%':'FLOAT',
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Source':'VARCHAR',
    'العجز_الكلي_نسبة_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Logic':'VARCHAR',
    'العجز_الكلي_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Comments':'VARCHAR',
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%':'FLOAT',
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Source':'VARCHAR',
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Logic':'VARCHAR',
    'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Comments':'VARCHAR',
    'عجز_ميزان_المدفوعات_بالمليون_دولار':'FLOAT',
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Source':'VARCHAR',
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Logic':'VARCHAR',
    'عجز_ميزان_المدفوعات_بالمليون_دولار_Comments':'VARCHAR',
    'الميزان_التجاري_بالمليار_دولار':'FLOAT',
    'الميزان_التجاري_بالمليار_دولار_Source':'VARCHAR',
    'الميزان_التجاري_بالمليار_دولار_Logic':'VARCHAR',
    'الميزان_التجاري_بالمليار_دولار_Comments':'VARCHAR',
    'قيمة_الواردات_بالمليار_دولار':'FLOAT',
    'قيمة_الواردات_بالمليار_دولار_Source':'VARCHAR',
    'قيمة_الواردات_بالمليار_دولار_Logic':'VARCHAR',
    'قيمة_الواردات_بالمليار_دولار_Comments':'VARCHAR',
    'قيمة_الصادرات_بالمليون_دولار':'FLOAT',
    'قيمة_الصادرات_بالمليون_دولار_Source':'VARCHAR',
    'قيمة_الصادرات_بالمليون_دولار_Logic':'VARCHAR',
    'قيمة_الصادرات_بالمليون_دولار_Comments':'VARCHAR',
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%':'FLOAT',
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Source':'VARCHAR',
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Logic':'VARCHAR',
    'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Comments':'VARCHAR',
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار':'FLOAT',
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Source':'VARCHAR',
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Logic':'VARCHAR',
    'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Comments':'VARCHAR',
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)':'VARCHAR',
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Source':'VARCHAR',
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Logic':'VARCHAR',
    'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Comments':'VARCHAR',
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)':'VARCHAR',
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Source':'VARCHAR',
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Logic':'VARCHAR',
    'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Comments':'VARCHAR',
    'احتياطات_النقد_الأجنبي_بالمليار_دولار':'FLOAT',
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Source':'VARCHAR',
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Logic':'VARCHAR',
    'احتياطات_النقد_الأجنبي_بالمليار_دولار_Comments':'VARCHAR',
    'نسبة_الفائدة_على_الودائع%':'FLOAT',
    'نسبة_الفائدة_على_الودائع%_Source':'VARCHAR',
    'نسبة_الفائدة_على_الودائع%_Logic':'VARCHAR',
    'نسبة_الفائدة_على_الودائع%_Comments':'VARCHAR',
    'نسبة_الفائدة_على_التسهيلات_الإئتمانية_للبنوك_المرخصة/كمبيالات%':'FLOAT',
    'نسبة_الفائدة_لتسهيلات_الإئتمانية_للبنوك/كمبيالات%_Source':'VARCHAR',
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/كمبيالات%_Logic':'VARCHAR',
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/كمبيالات%_Comments':'VARCHAR',
    'نسبة_الفائدة_على_التسهيلات_الإئتمانية_للبنوك_المرخصة/جاري-مدين%':'FLOAT',
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Source':'VARCHAR',
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Logic':'VARCHAR',
    'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Comments':'VARCHAR',
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار':'FLOAT',
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Source':'VARCHAR',
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Logic':'VARCHAR',
    'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Comments':'VARCHAR',
    'نسبة_ضريبة_المبيعات%':'FLOAT',
    'نسبة_ضريبة_المبيعات%_Source':'VARCHAR',
    'نسبة_ضريبة_المبيعات%_Logic':'VARCHAR',
    'نسبة_ضريبة_المبيعات%_Comments':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الفرد%':'FLOAT',
    'نسبة_ضريبة_الدخل_على_الفرد%_Source':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الفرد%_Logic':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الفرد%_Comments':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الشركات%':'FLOAT',
    'نسبة_ضريبة_الدخل_على_الشركات%_Source':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الشركات%_Logic':'VARCHAR',
    'نسبة_ضريبة_الدخل_على_الشركات%_Comments':'VARCHAR',
    'ضريبة_الأرباح%':'FLOAT',
    'ضريبة_الأرباح%_Source':'VARCHAR',
    'ضريبة_الأرباح%_Logic':'VARCHAR',
    'ضريبة_الأرباح%_Comments':'VARCHAR',
    'ضريبة_الارباح_قطاع_البنوك%':'FLOAT',
    'ضريبة_الارباح_قطاع_البنوك%_Source':'VARCHAR',
    'ضريبة_الارباح_قطاع_البنوك%_Logic':'VARCHAR',
    'ضريبة_الارباح_قطاع_البنوك%_Comments':'VARCHAR',
    'مؤشر_الفساد':'FLOAT',
    'مؤشر_الفساد_Source':'VARCHAR',
    'مؤشر_الفساد_Logic':'VARCHAR',
    'مؤشر_الفساد_Comments':'VARCHAR',
    'الترتيب_العالمي_على_مؤشر_الفساد':'FLOAT',
    'الترتيب_العالمي_على_مؤشر_الفساد_Source':'VARCHAR',
    'الترتيب_العالمي_على_مؤشر_الفساد_Logic':'VARCHAR',
    'الترتيب_العالمي_على_مؤشر_الفساد_Comments':'VARCHAR',
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال':'FLOAT',
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Source':'VARCHAR',
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Logic':'VARCHAR',
    'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Comments':'VARCHAR',
    'كثافة_مؤسسات_الأعمال_الجديدة':'FLOAT',
    'كثافة_مؤسسات_الأعمال_الجديدة_Source':'VARCHAR',
    'كثافة_مؤسسات_الأعمال_الجديدة_Logic':'VARCHAR',
    'كثافة_مؤسسات_الأعمال_الجديدة_Comments':'VARCHAR',
    'S&P_التصنيف_الائتماني_حسب_مؤشر':'VARCHAR',
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Source':'VARCHAR',
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Logic':'VARCHAR',
    'S&P_التصنيف_الائتماني_حسب_مؤشر_Comments':'VARCHAR',
    "Moody's_التصنيف_الائتماني_حسب_مؤشر":'VARCHAR',
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Source":'VARCHAR',
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Logic":'VARCHAR',
    "Moody's_التصنيف_الائتماني_حسب_مؤشر_Comments":'VARCHAR',
    'Fitch_التصنيف_الائتماني_حسب_مؤشر':'VARCHAR',
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Source':'VARCHAR',
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Logic':'VARCHAR',
    'Fitch_التصنيف_الائتماني_حسب_مؤشر_Comments':'VARCHAR',
    'أبرز_الصادرات':'VARCHAR',
    'أبرز_الصادرات_Source':'VARCHAR',
    'أبرز_الصادرات_Logic':'VARCHAR',
    'أبرز_الصادرات_Comments':'VARCHAR',
    'أبرز_الواردات':'VARCHAR',
    'أبرز_الواردات_Source':'VARCHAR',
    'أبرز_الواردات_Logic':'VARCHAR',
    'أبرز_الواردات_Comments':'VARCHAR',
    'السنة':'INT',
    'الناتج_المحلي_الإجمالي_مليار$_Actual':'FLOAT',
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Source':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Formula':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Logic':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Actual_Comments':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Weight':'FLOAT',
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Formula':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Logic':'VARCHAR',
    'الناتج_المحلي_الإجمالي_مليار$_Weight_Comments':'VARCHAR',
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual':'FLOAT',
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Source':'VARCHAR',
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Formula':'VARCHAR',
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Logic':'VARCHAR',
    '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Comments':'VARCHAR',
    'النمو_في_الناتج_المحلي_الإجمالي_Weight':'FLOAT',
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Formula':'VARCHAR',
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Logic':'VARCHAR',
    'النمو_في_الناتج_المحلي_الإجمالي_Weight_Comments':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي%_Actual':'FLOAT',
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Source':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Formula':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Logic':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي%_Actual_Comments':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي_Weight':'FLOAT',
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Formula':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Logic':'VARCHAR',
    'النمو_في_الإنفاق_الاستهلاكي_Weight_Comments':'VARCHAR',
    'نمو_الاستثمار%_Actual':'FLOAT',
    'نمو_الاستثمار%_Actual_Source':'VARCHAR',
    'نمو_الاستثمار%_Actual_Formula':'VARCHAR',
    'نمو_الاستثمار%_Actual_Logic':'VARCHAR',
    'نمو_الاستثمار%_Actual_Comments':'VARCHAR',
    'نمو_الاستثمار_Weight':'FLOAT',
    'نمو_الاستثمار_Weight_Formula':'VARCHAR',
    'نمو_الاستثمار_Weight_Logic':'VARCHAR',
    'نمو_الاستثمار_Weight_Comments':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي%_Actual':'FLOAT',
    'النمو_في_الإنفاق_الحكومي%_Actual_Source':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي%_Actual_Formula':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي%_Actual_Logic':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي%_Actual_Comments':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي_Weight':'FLOAT',
    'النمو_في_الإنفاق_الحكومي_Weight_Formula':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي_Weight_Logic':'VARCHAR',
    'النمو_في_الإنفاق_الحكومي_Weight_Comments':'VARCHAR',
    'العجز_المالي_الحكومي%_Actual':'FLOAT',
    'العجز_المالي_الحكومي%_Actual_Source':'VARCHAR',
    'العجز_المالي_الحكومي%_Actual_Formula':'VARCHAR',
    'العجز_المالي_الحكومي%_Actual_Logic':'VARCHAR',
    'العجز_المالي_الحكومي%_Actual_Comments':'VARCHAR',
    'العجز_المالي_الحكومي_Weight':'FLOAT',
    'العجز_المالي_الحكومي_Weight_Formula':'VARCHAR',
    'العجز_المالي_الحكومي_Weight_Logic':'VARCHAR',
    'العجز_المالي_الحكومي_Weight_Comments':'VARCHAR',
    'GDP%_الدين_الحكومي_Actual':'FLOAT',
    'GDP%_الدين_الحكومي_Actual_Source':'VARCHAR',
    'GDP%_الدين_الحكومي_Actual_Formula':'VARCHAR',
    'GDP%_الدين_الحكومي_Actual_Logic':'VARCHAR',
    'GDP%_الدين_الحكومي_Actual_Comments':'VARCHAR',
    'الدين_الحكومي_Weight':'FLOAT',
    'الدين_الحكومي_Weight_Formula':'VARCHAR',
    'الدين_الحكومي_Weight_Logic':'VARCHAR',
    'الدين_الحكومي_Weight_Comments':'VARCHAR',
    'النمو_في_القوة_العمالية_Actual':'FLOAT',
    'النمو_في_القوة_العمالية_Actual_Source':'VARCHAR',
    'النمو_في_القوة_العمالية_Actual_Formula':'VARCHAR',
    'النمو_في_القوة_العمالية_Actual_Logic':'VARCHAR',
    'النمو_في_القوة_العمالية_Actual_Comments':'VARCHAR',
    'النمو_في_القوة_العمالية_Weight':'FLOAT',
    'النمو_في_القوة_العمالية_Weight_Formula':'VARCHAR',
    'النمو_في_القوة_العمالية_Weight_Logic':'VARCHAR',
    'النمو_في_القوة_العمالية_Weight_Comments':'VARCHAR',
    'دين_القطاع_الخاص%_Actual':'FLOAT',
    'دين_القطاع_الخاص%_Actual_Source':'VARCHAR',
    'دين_القطاع_الخاص%_Actual_Formula':'VARCHAR',
    'دين_القطاع_الخاص%_Actual_Logic':'VARCHAR',
    'دين_القطاع_الخاص%_Actual_Comments':'VARCHAR',
    'دين_القطاع_الخاص_Weight':'FLOAT',
    'دين_القطاع_الخاص_Weight_Formula':'VARCHAR',
    'دين_القطاع_الخاص_Weight_Logic':'VARCHAR',
    'دين_القطاع_الخاص_Weight_Comments':'VARCHAR',
    'نمو_الصادرات%_Actual':'FLOAT',
    'نمو_الصادرات%_Actual_Source':'VARCHAR',
    'نمو_الصادرات%_Actual_Formula':'VARCHAR',
    'نمو_الصادرات%_Actual_Logic':'VARCHAR',
    'نمو_الصادرات%_Actual_Comments':'VARCHAR',
    'نمو_الصادرات_Weight':'FLOAT',
    'نمو_الصادرات_Weight_Formula':'VARCHAR',
    'نمو_الصادرات_Weight_Logic':'VARCHAR',
    'نمو_الصادرات_Weight_Comments':'VARCHAR',
    'نمو_الواردات%_Actual':'FLOAT',
    'نمو_الواردات%_Actual_Source':'VARCHAR',
    'نمو_الواردات%_Actual_Formula':'VARCHAR',
    'نمو_الواردات%_Actual_Logic':'VARCHAR',
    'نمو_الواردات%_Actual_Comments':'VARCHAR',
    'نمو_الواردات_Weight':'FLOAT',
    'نمو_الواردات_Weight_Formula':'VARCHAR',
    'نمو_الواردات_Weight_Logic':'VARCHAR',
    'نمو_الواردات_Weight_Comments':'VARCHAR',
    'الاستقرار_النقدي_Actual':'VARCHAR',
    'الاستقرار_النقدي_Actual_Source':'VARCHAR',
    'الاستقرار_النقدي_Actual_Formula':'VARCHAR',
    'الاستقرار_النقدي_Actual_Logic':'VARCHAR',
    'الاستقرار_النقدي_Actual_Comments':'VARCHAR',
    'الاستقرار_النقدي_Weight':'FLOAT',
    'الاستقرار_النقدي_Weight_Formula':'VARCHAR',
    'الاستقرار_النقدي_Weight_Logic':'VARCHAR',
    'الاستقرار_النقدي_Weight_Comments':'VARCHAR',
    'إجمالي_تكوين_رأس_المال%_Actual':'FLOAT',
    'إجمالي_تكوين_رأس_المال%_Actual_Source':'VARCHAR',
    'إجمالي_تكوين_رأس_المال%_Actual_Formula':'VARCHAR',
    'إجمالي_تكوين_رأس_المال%_Actual_Logic':'VARCHAR',
    'إجمالي_تكوين_رأس_المال%_Actual_Comments':'VARCHAR',
    'إجمالي_تكوين_رأس_المال_Weight':'FLOAT',
    'إجمالي_تكوين_رأس_المال_Weight_Formula':'VARCHAR',
    'إجمالي_تكوين_رأس_المال_Weight_Logic':'VARCHAR',
    'إجمالي_تكوين_رأس_المال_Weight_Comments':'VARCHAR',
    'GDP%_صافي_الاستثمار_الأجنبي_Actual':'FLOAT',
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Source':'VARCHAR',
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Formula':'VARCHAR',
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Logic':'VARCHAR',
    'GDP%_صافي_الاستثمار_الأجنبي_Actual_Comments':'VARCHAR',
    'صافي_الاستثمار_الأجنبي_Weight':'FLOAT',
    'صافي_الاستثمار_الأجنبي_Weight_Formula':'VARCHAR',
    'صافي_الاستثمار_الأجنبي_Weight_Logic':'VARCHAR',
    'صافي_الاستثمار_الأجنبي_Weight_Comments':'VARCHAR',
    'تعزيز_الانتاجية%_Actual':'FLOAT',
    'تعزيز_الانتاجية%_Actual_Source':'VARCHAR',
    'تعزيز_الانتاجية%_Actual_Formula':'VARCHAR',
    'تعزيز_الانتاجية%_Actual_Logic':'VARCHAR',
    'تعزيز_الانتاجية%_Actual_Comments':'VARCHAR',
    'تعزيز_الانتاجية_Weight':'FLOAT',
    'تعزيز_الانتاجية_Weight_Formula':'VARCHAR',
    'تعزيز_الانتاجية_Weight_Logic':'VARCHAR',
    'تعزيز_الانتاجية_Weight_Comments':'VARCHAR',
    'المجموع':'FLOAT',
    'المجموع_Formula':'VARCHAR',
    'المجموع_Logic':'VARCHAR',
    'المجموع_Comments':'VARCHAR',
    'إيرادات_الناتج_المحلي_الإجمالي':'VARCHAR',
    'إيرادات_الناتج_المحلي_الإجمالي_Sources':'VARCHAR',
    'إيرادات_الناتج_المحلي_الإجمالي_Logic':'VARCHAR',
    'إيرادات_الناتج_المحلي_الإجمالي_Comments':'VARCHAR',
    'إيرادات_الموازنة_العامة':'VARCHAR',
    'إيرادات_الموازنة_العامة_Sources':'VARCHAR',
    'إيرادات_الموازنة_العامة_Logic':'VARCHAR',
    'إيرادات_الموازنة_العامة_Comments':'VARCHAR',
    'نفقات_الموازنة_العامة':'VARCHAR',
    'نفقات_الموازنة_العامة_Sources':'VARCHAR',
    'نفقات_الموازنة_العامة_Logic':'VARCHAR',
    'نفقات_الموازنة_العامة_Comments':'VARCHAR',
    '(GDP%)_الاستثمار_Actual':'FLOAT',
    '(GDP%)_الاستثمار_Actual_Source':'VARCHAR',
    '(GDP%)_الاستثمار_Actual_Formula':'VARCHAR',
    '(GDP%)_الاستثمار_Actual_Logic':'VARCHAR',
    '(GDP%)_الاستثمار_Actual_Comments':'VARCHAR',
    '(GDP%)_الاستثمار_Weight':'FLOAT',
    '(GDP%)_الاستثمار_Weight_Formula':'VARCHAR',
    '(GDP%)_الاستثمار_Weight_Logic':'VARCHAR',
    '(GDP%)_الاستثمار_Weight_Comments':'VARCHAR',
    'نمو_الاستثمار_Actual':'FLOAT',
    'نمو_الاستثمار_Actual_Source':'VARCHAR',
    'نمو_الاستثمار_Actual_Formula':'VARCHAR',
    'نمو_الاستثمار_Actual_Logic':'VARCHAR',
    'نمو_الاستثمار_Actual_Comments':'VARCHAR',
    'نمو_الاستثمار_Weight':'FLOAT',
    'نمو_الاستثمار_Weight_Formula':'VARCHAR',
    'نمو_الاستثمار_Weight_Logic':'VARCHAR',
    'نمو_الاستثمار_Weight_Comments':'VARCHAR',
    '%الابتكار_في_الاقتصاد_Actual':'FLOAT',
    '%الابتكار_في_الاقتصاد_Actual_Source':'VARCHAR',
    '%الابتكار_في_الاقتصاد_Actual_Formula':'VARCHAR',
    '%الابتكار_في_الاقتصاد_Actual_Logic':'VARCHAR',
    '%الابتكار_في_الاقتصاد_Actual_Comments':'VARCHAR',
    'الابتكار_في_الاقتصاد_Weight':'FLOAT',
    'الابتكار_في_الاقتصاد_Weight_Formula':'VARCHAR',
    'الابتكار_في_الاقتصاد_Weight_Logic':'VARCHAR',
    'الابتكار_في_الاقتصاد_Weight_Comments':'VARCHAR',
    '%الفائدة_على_الإقراض_Actual':'FLOAT',
    '%الفائدة_على_الإقراض_Actual_Source':'VARCHAR',
    '%الفائدة_على_الإقراض_Actual_Formula':'VARCHAR',
    '%الفائدة_على_الإقراض_Actual_Logic':'VARCHAR',
    '%الفائدة_على_الإقراض_Actual_Comments':'VARCHAR',
    'الفائدة_على_الإقراض_Weight':'FLOAT',
    'الفائدة_على_الإقراض_Weight_Formula':'VARCHAR',
    'الفائدة_على_الإقراض_Weight_Logic':'VARCHAR',
    'الفائدة_على_الإقراض_Weight_Comments':'VARCHAR',
    'النمو_السكاني%_Actual':'FLOAT',
    'النمو_السكاني%_Actual_Source':'VARCHAR',
    'النمو_السكاني%_Actual_Formula':'VARCHAR',
    'النمو_السكاني%_Actual_Logic':'VARCHAR',
    'النمو_السكاني%_Actual_Comments':'VARCHAR',
    'النمو_السكاني_Weight':'FLOAT',
    'النمو_السكاني_Weight_Formula':'VARCHAR',
    'النمو_السكاني_Weight_Logic':'VARCHAR',
    'النمو_السكاني_Weight_Comments':'VARCHAR',
    'نمو_القوة_العمالية%_Actual':'FLOAT',
    'نمو_القوة_العمالية%_Actual_Source':'VARCHAR',
    'نمو_القوة_العمالية%_Actual_Formula':'VARCHAR',
    'نمو_القوة_العمالية%_Actual_Logic':'VARCHAR',
    'نمو_القوة_العمالية%_Actual_Comments':'VARCHAR',
    'نمو_القوة_العمالية_Weight':'FLOAT',
    'نمو_القوة_العمالية_Weight_Formula':'VARCHAR',
    'نمو_القوة_العمالية_Weight_Logic':'VARCHAR',
    'نمو_القوة_العمالية_Weight_Comments':'VARCHAR',
    'الفائدة_على_الودائع%_Actual':'FLOAT',
    'الفائدة_على_الودائع%_Actual_Source':'VARCHAR',
    'الفائدة_على_الودائع%_Actual_Formula':'VARCHAR',
    'الفائدة_على_الودائع%_Actual_Logic':'VARCHAR',
    'الفائدة_على_الودائع%_Actual_Comments':'VARCHAR',
    'الفائدة_على_الودائع_Weight':'FLOAT',
    'الفائدة_على_الودائع_Weight_Formula':'VARCHAR',
    'الفائدة_على_الودائع_Weight_Logic':'VARCHAR',
    'الفائدة_على_الودائع_Weight_Comments':'VARCHAR',
    'التضخم_Actual':'FLOAT',
    'التضخم_Actual_Source':'VARCHAR',
    'التضخم_Actual_Formula':'VARCHAR',
    'التضخم_Actual_Logic':'VARCHAR',
    'التضخم_Actual_Comments':'VARCHAR',
    'التضخم_Weight':'FLOAT',
    'التضخم_Weight_Formula':'VARCHAR',
    'التضخم_Weight_Logic':'VARCHAR',
    'التضخم_Weight_Comments':'VARCHAR',
    'الاستقرار_النقدي_Actual':'VARCHAR',
    'الاستقرار_النقدي_Actual_Source':'VARCHAR',
    'الاستقرار_النقدي_Actual_Formula':'VARCHAR',
    'الاستقرار_النقدي_Actual_Logic':'VARCHAR',
    'الاستقرار_النقدي_Actual_Comments':'VARCHAR',
    'الاستقرار_النقدي_Weight':'FLOAT',
    'الاستقرار_النقدي_Weight_Formula':'VARCHAR',
    'الاستقرار_النقدي_Weight_Logic':'VARCHAR',
    'الاستقرار_النقدي_Weight_Comments':'VARCHAR',
    'استقلالية_البنك_المركزي_Actual':'VARCHAR',
    'استقلالية_البنك_المركزي_Actual_Source':'VARCHAR',
    'استقلالية_البنك_المركزي_Actual_Formula':'VARCHAR',
    'استقلالية_البنك_المركزي_Actual_Logic':'VARCHAR',
    'استقلالية_البنك_المركزي_Actual_Comments':'VARCHAR',
    'استقلالية_البنك_المركزي_Weight':'FLOAT',
    'استقلالية_البنك_المركزي_Weight_Formula':'VARCHAR',
    'استقلالية_البنك_المركزي_Weight_Logic':'VARCHAR',
    'استقلالية_البنك_المركزي_Weight_Comments':'VARCHAR',
    'نمو_الصادرات%_Actual':'FLOAT',
    'نمو_الصادرات%_Actual_Source':'VARCHAR',
    'نمو_الصادرات%_Actual_Formula':'VARCHAR',
    'نمو_الصادرات%_Actual_Logic':'VARCHAR',
    'نمو_الصادرات%_Actual_Comments':'VARCHAR',
    'نمو_الصادرات%_Weight':'FLOAT',
    'نمو_الصادرات%_Weight_Formula':'VARCHAR',
    'نمو_الصادرات%_Weight_Logic':'VARCHAR',
    'نمو_الصادرات%_Weight_Comments':'VARCHAR',
    'نمو_الواردات%_Actual':'FLOAT',
    'نمو_الواردات%_Actual_Source':'VARCHAR',
    'نمو_الواردات%_Actual_Formula':'VARCHAR',
    'نمو_الواردات%_Actual_Logic':'VARCHAR',
    'نمو_الواردات%_Actual_Comments':'VARCHAR',
    'نمو_الواردات%_Weight':'FLOAT',
    'نمو_الواردات%_Weight_Formula':'VARCHAR',
    'نمو_الواردات%_Weight_Logic':'VARCHAR',
    'نمو_الواردات%_Weight_Comments':'VARCHAR',
    'الميزان_التجاري_مليار$_Actual':'FLOAT',
    'الميزان_التجاري_مليار$_Actual_Source':'VARCHAR',
    'الميزان_التجاري_مليار$_Actual_Formula':'VARCHAR',
    'الميزان_التجاري_مليار$_Actual_Logic':'VARCHAR',
    'الميزان_التجاري_مليار$_Actual_Comments':'VARCHAR',
    'الميزان_التجاري_مليار$_Weight':'FLOAT',
    'الميزان_التجاري_مليار$_Weight_Formula':'VARCHAR',
    'الميزان_التجاري_مليار$_Weight_Logic':'VARCHAR',
    'الميزان_التجاري_مليار$_Weight_Comments':'VARCHAR',
    'العجز_النقدي%_Actual':'FLOAT',
    'العجز_النقدي%_Actual_Source':'VARCHAR',
    'العجز_النقدي%_Actual_Formula':'VARCHAR',
    'العجز_النقدي%_Actual_Logic':'VARCHAR',
    'العجز_النقدي%_Actual_Comments':'VARCHAR',
    'العجز_النقدي_Weight':'FLOAT',
    'العجز_النقدي_Weight_Formula':'VARCHAR',
    'العجز_النقدي_Weight_Logic':'VARCHAR',
    'العجز_النقدي_Weight_Comments':'VARCHAR',
    '(GDP%)_الدين_الخارجي_Actual':'FLOAT',
    '(GDP%)_الدين_الخارجي_Actual_Source':'VARCHAR',
    '(GDP%)_الدين_الخارجي_Actual_Formula':'VARCHAR',
    '(GDP%)_الدين_الخارجي_Actual_Logic':'VARCHAR',
    '(GDP%)_الدين_الخارجي_Actual_Comments':'VARCHAR',
    'الدين_الخارجي_Weight':'FLOAT',
    'الدين_الخارجي_Weight_Formula':'VARCHAR',
    'الدين_الخارجي_Weight_Logic':'VARCHAR',
    'الدين_الخارجي_Weight_Comments':'VARCHAR',
    'القطاع':'VARCHAR',
    'القطاع_الفرعي':'VARCHAR',
    'العنوان':'VARCHAR',
    'الوصف':'VARCHAR',
    'التكلفة_التقريبية':'VARCHAR',
    'العائد_على_الاستثمار':'VARCHAR',
    '%استقرار_الاقتصاد_الكلي_Actual':'FLOAT',
    '%استقرار_الاقتصاد_الكلي_Actual_Source':'VARCHAR',
    '%استقرار_الاقتصاد_الكلي_Actual_Formula':'VARCHAR',
    '%استقرار_الاقتصاد_الكلي_Actual_Logic':'VARCHAR',
    '%استقرار_الاقتصاد_الكلي_Actual_Comments':'VARCHAR',
    'استقرار_الاقتصاد_الكلي_Weight':'FLOAT',
    'استقرار_الاقتصاد_الكلي_Weight_Formula':'VARCHAR',
    'استقرار_الاقتصاد_الكلي_Weight_Logic':'VARCHAR',
    'استقرار_الاقتصاد_الكلي_Weight_Comments':'VARCHAR',
    'عدم_اليقين_في_السياسات%_Actual':'FLOAT',
    'عدم_اليقين_في_السياسات%_Actual_Source':'VARCHAR',
    'عدم_اليقين_في_السياسات%_Actual_Formula':'VARCHAR',
    'عدم_اليقين_في_السياسات%_Actual_Logic':'VARCHAR',
    'عدم_اليقين_في_السياسات%_Actual_Comments':'VARCHAR',
    'عدم_اليقين_في_السياسات_Weight':'FLOAT',
    'عدم_اليقين_في_السياسات_Weight_Formula':'VARCHAR',
    'عدم_اليقين_في_السياسات_Weight_Logic':'VARCHAR',
    'عدم_اليقين_في_السياسات_Weight_Comments':'VARCHAR',
    'الفساد%_Actual':'FLOAT',
    'الفساد%_Actual_Source':'VARCHAR',
    'الفساد%_Actual_Formula':'VARCHAR',
    'الفساد%_Actual_Logic':'VARCHAR',
    'الفساد%_Actual_Comments':'VARCHAR',
    'الفساد_Weight':'FLOAT',
    'الفساد_Weight_Formula':'VARCHAR',
    'الفساد_Weight_Logic':'VARCHAR',
    'الفساد_Weight_Comments':'VARCHAR',
    'معدل_الضرائب%_Actual':'FLOAT',
    'معدل_الضرائب%_Actual_Source':'VARCHAR',
    'معدل_الضرائب%_Actual_Formula':'VARCHAR',
    'معدل_الضرائب%_Actual_Logic':'VARCHAR',
    'معدل_الضرائب%_Actual_Comments':'VARCHAR',
    'معدل_الضرائب_Weight':'FLOAT',
    'معدل_الضرائب_Weight_Formula':'VARCHAR',
    'معدل_الضرائب_Weight_Logic':'VARCHAR',
    'معدل_الضرائب_Weight_Comments':'VARCHAR',
    'التكلفة_والحصول_على_التمويل%_Actual':'FLOAT',
    'التكلفة_والحصول_على_التمويل%_Actual_Source':'VARCHAR',
    'التكلفة_والحصول_على_التمويل%_Actual_Formula':'VARCHAR',
    'التكلفة_والحصول_على_التمويل%_Actual_Logic':'VARCHAR',
    'التكلفة_والحصول_على_التمويل%_Actual_Comments':'VARCHAR',
    'التكلفة_والحصول_على_التمويل_Weight':'FLOAT',
    'التكلفة_والحصول_على_التمويل_Weight_Formula':'VARCHAR',
    'التكلفة_والحصول_على_التمويل_Weight_Logic':'VARCHAR',
    'التكلفة_والحصول_على_التمويل_Weight_Comments':'VARCHAR',
    'الجريمة%_Actual':'FLOAT',
    'الجريمة%_Actual_Source':'VARCHAR',
    'الجريمة%_Actual_Formula':'VARCHAR',
    'الجريمة%_Actual_Logic':'VARCHAR',
    'الجريمة%_Actual_Comments':'VARCHAR',
    'الجريمة_Weight':'FLOAT',
    'الجريمة_Weight_Formula':'VARCHAR',
    'الجريمة_Weight_Logic':'VARCHAR',
    'الجريمة_Weight_Comments':'VARCHAR',
    'اللوائح_وإدارة_الضرائب%_Actual':'FLOAT',
    'اللوائح_وإدارة_الضرائب%_Actual_Source':'VARCHAR',
    'اللوائح_وإدارة_الضرائب%_Actual_Formula':'VARCHAR',
    'اللوائح_وإدارة_الضرائب%_Actual_Logic':'VARCHAR',
    'اللوائح_وإدارة_الضرائب%_Actual_Comments':'VARCHAR',
    'اللوائح_وإدارة_الضرائب_Weight':'FLOAT',
    'اللوائح_وإدارة_الضرائب_Weight_Formula':'VARCHAR',
    'اللوائح_وإدارة_الضرائب_Weight_Logic':'VARCHAR',
    'اللوائح_وإدارة_الضرائب_Weight_Comments':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Actual':'FLOAT',
    'المهارات_الأساسية_في_الاقتصاد_Actual_Source':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Actual_Formula':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Actual_Logic':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Actual_Comments':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Weight':'FLOAT',
    'المهارات_الأساسية_في_الاقتصاد_Weight_Formula':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Weight_Logic':'VARCHAR',
    'المهارات_الأساسية_في_الاقتصاد_Weight_Comments':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي%_Actual':'FLOAT',
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Source':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Formula':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Logic':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي%_Actual_Comments':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي_Weight':'FLOAT',
    'جودة_التعليم_الابتدائي_والعالي_Weight_Formula':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي_Weight_Logic':'VARCHAR',
    'جودة_التعليم_الابتدائي_والعالي_Weight_Comments':'VARCHAR',
    'جودة_العناية_الصحية%_Actual':'FLOAT',
    'جودة_العناية_الصحية%_Actual_Source':'VARCHAR',
    'جودة_العناية_الصحية%_Actual_Formula':'VARCHAR',
    'جودة_العناية_الصحية%_Actual_Logic':'VARCHAR',
    'جودة_العناية_الصحية%_Actual_Comments':'VARCHAR',
    'جودة_العناية_الصحية_Weight':'FLOAT',
    'جودة_العناية_الصحية_Weight_Formula':'VARCHAR',
    'جودة_العناية_الصحية_Weight_Logic':'VARCHAR',
    'جودة_العناية_الصحية_Weight_Comments':'VARCHAR',
    '%نظام_المحاكم_Actual':'FLOAT',
    '%نظام_المحاكم_Actual_Source':'VARCHAR',
    '%نظام_المحاكم_Actual_Formula':'VARCHAR',
    '%نظام_المحاكم_Actual_Logic':'VARCHAR',
    '%نظام_المحاكم_Actual_Comments':'VARCHAR',
    'نظام_المحاكم_Weight':'FLOAT',
    'نظام_المحاكم_Weight_Formula':'VARCHAR',
    'نظام_المحاكم_Weight_Logic':'VARCHAR',
    'نظام_المحاكم_Weight_Comments':'VARCHAR',
    'النقل%_Actual':'FLOAT',
    'النقل%_Actual_Source':'VARCHAR',
    'النقل%_Actual_Formula':'VARCHAR',
    'النقل%_Actual_Logic':'VARCHAR',
    'النقل%_Actual_Comments':'VARCHAR',
    'النقل_Weight':'FLOAT',
    'النقل_Weight_Formula':'VARCHAR',
    'النقل_Weight_Logic':'VARCHAR',
    'النقل_Weight_Comments':'VARCHAR',
    'الاتصالات%_Actual':'FLOAT',
    'الاتصالات%_Actual_Source':'VARCHAR',
    'الاتصالات%_Actual_Formula':'VARCHAR',
    'الاتصالات%_Actual_Logic':'VARCHAR',
    'الاتصالات%_Actual_Comments':'VARCHAR',
    'الاتصالات_Weight':'FLOAT',
    'الاتصالات_Weight_Formula':'VARCHAR',
    'الاتصالات_Weight_Logic':'VARCHAR',
    'الاتصالات_Weight_Comments':'VARCHAR',
    'الرقمنة_Actual':'FLOAT',
    'الرقمنة_Actual_Source':'VARCHAR',
    'الرقمنة_Actual_Formula':'VARCHAR',
    'الرقمنة_Actual_Logic':'VARCHAR',
    'الرقمنة_Actual_Comments':'VARCHAR',
    'الرقمنة_Weight':'FLOAT',
    'الرقمنة_Weight_Formula':'VARCHAR',
    'الرقمنة_Weight_Logic':'VARCHAR',
    'الرقمنة_Weight_Comments':'VARCHAR',
    'تكاليف_المعيشة%_Actual':'FLOAT',
    'تكاليف_المعيشة%_Actual_Source':'VARCHAR',
    'تكاليف_المعيشة%_Actual_Formula':'VARCHAR',
    'تكاليف_المعيشة%_Actual_Logic':'VARCHAR',
    'تكاليف_المعيشة%_Actual_Comments':'VARCHAR',
    'تكاليف_المعيشة_Weight':'FLOAT',
    'تكاليف_المعيشة_Weight_Formula':'VARCHAR',
    'تكاليف_المعيشة_Weight_Logic':'VARCHAR',
    'تكاليف_المعيشة_Weight_Comments':'VARCHAR',
    'جودة_المعيشة%_Actual':'FLOAT',
    'جودة_المعيشة%_Actual_Source':'VARCHAR',
    'جودة_المعيشة%_Actual_Formula':'VARCHAR',
    'جودة_المعيشة%_Actual_Logic':'VARCHAR',
    'جودة_المعيشة%_Actual_Comments':'VARCHAR',
    'جودة_المعيشة_Weight':'FLOAT',
    'جودة_المعيشة_Weight_Formula':'VARCHAR',
    'جودة_المعيشة_Weight_Logic':'VARCHAR',
    'جودة_المعيشة_Weight_Comments':'VARCHAR',
    'GPI_السلام_العالمي_Actual':'FLOAT',
    'GPI_السلام_العالمي_Actual_Source':'VARCHAR',
    'GPI_السلام_العالمي_Actual_Formula':'VARCHAR',
    'GPI_السلام_العالمي_Actual_Logic':'VARCHAR',
    'GPI_السلام_العالمي_Actual_Comments':'VARCHAR',
    'GPI_السلام_العالمي_Weight':'FLOAT',
    'GPI_السلام_العالمي_Weight_Formula':'VARCHAR',
    'GPI_السلام_العالمي_Weight_Logic':'VARCHAR',
    'GPI_السلام_العالمي_Weight_Comments':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Actual':'FLOAT',
    'PSI_الاستقرار_السياسي_العالمي_Actual_Source':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Actual_Formula':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Actual_Logic':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Actual_Comments':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Weight':'FLOAT',
    'PSI_الاستقرار_السياسي_العالمي_Weight_Formula':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Weight_Logic':'VARCHAR',
    'PSI_الاستقرار_السياسي_العالمي_Weight_Comments':'VARCHAR',
    'CPI_مدركات_الفساد_Actual':'FLOAT',
    'CPI_مدركات_الفساد_Actual_Source':'VARCHAR',
    'CPI_مدركات_الفساد_Actual_Formula':'VARCHAR',
    'CPI_مدركات_الفساد_Actual_Logic':'VARCHAR',
    'CPI_مدركات_الفساد_Actual_Comments':'VARCHAR',
    'CPI_مدركات_الفساد_Weight':'FLOAT',
    'CPI_مدركات_الفساد_Weight_Formula':'VARCHAR',
    'CPI_مدركات_الفساد_Weight_Logic':'VARCHAR',
    'CPI_مدركات_الفساد_Weight_Comments':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Actual':'FLOAT',
    'GTI_مكافحة_الإرهاب_Actual_Source':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Actual_Formula':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Actual_Logic':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Actual_Comments':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Weight':'FLOAT',
    'GTI_مكافحة_الإرهاب_Weight_Formula':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Weight_Logic':'VARCHAR',
    'GTI_مكافحة_الإرهاب_Weight_Comments':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Actual':'FLOAT',
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Source':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Formula':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Logic':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Actual_Comments':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Weight':'FLOAT',
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Formula':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Logic':'VARCHAR',
    'WRI_مخاطر_الكوارث_الطبيعية_Weight_Comments':'VARCHAR',
    'HDI_التنمية_البشرية_Actual':'FLOAT',
    'HDI_التنمية_البشرية_Actual_Source':'VARCHAR',
    'HDI_التنمية_البشرية_Actual_Formula':'VARCHAR',
    'HDI_التنمية_البشرية_Actual_Logic':'VARCHAR',
    'HDI_التنمية_البشرية_Actual_Comments':'VARCHAR',
    'HDI_التنمية_البشرية_Weight':'FLOAT',
    'HDI_التنمية_البشرية_Weight_Formula':'VARCHAR',
    'HDI_التنمية_البشرية_Weight_Logic':'VARCHAR',
    'HDI_التنمية_البشرية_Weight_Comments':'VARCHAR',
    'TI_الشفافية_العالمي_Actual':'FLOAT',
    'TI_الشفافية_العالمي_Actual_Source':'VARCHAR',
    'TI_الشفافية_العالمي_Actual_Formula':'VARCHAR',
    'TI_الشفافية_العالمي_Actual_Logic':'VARCHAR',
    'TI_الشفافية_العالمي_Actual_Comments':'VARCHAR',
    'TI_الشفافية_العالمي_Weight':'FLOAT',
    'TI_الشفافية_العالمي_Weight_Formula':'VARCHAR',
    'TI_الشفافية_العالمي_Weight_Logic':'VARCHAR',
    'TI_الشفافية_العالمي_Weight_Comments':'VARCHAR',
    'BEI_بيئة_الأعمال_Actual':'FLOAT',
    'BEI_بيئة_الأعمال_Actual_Source':'VARCHAR',
    'BEI_بيئة_الأعمال_Actual_Formula':'VARCHAR',
    'BEI_بيئة_الأعمال_Actual_Logic':'VARCHAR',
    'BEI_بيئة_الأعمال_Actual_Comments':'VARCHAR',
    'BEI_بيئة_الأعمال_Weight':'FLOAT',
    'BEI_بيئة_الأعمال_Weight_Formula':'VARCHAR',
    'BEI_بيئة_الأعمال_Weight_Logic':'VARCHAR',
    'BEI_بيئة_الأعمال_Weight_Comments':'VARCHAR',
    'WJP_سيادة_القانون_Actual':'FLOAT',
    'WJP_سيادة_القانون_Actual_Source':'VARCHAR',
    'WJP_سيادة_القانون_Actual_Formula':'VARCHAR',
    'WJP_سيادة_القانون_Actual_Logic':'VARCHAR',
    'WJP_سيادة_القانون_Actual_Comments':'VARCHAR',
    'WJP_سيادة_القانون_Weight':'FLOAT',
    'WJP_سيادة_القانون_Weight_Formula':'VARCHAR',
    'WJP_سيادة_القانون_Weight_Logic':'VARCHAR',
    'WJP_سيادة_القانون_Weight_Comments':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Actual':'FLOAT',
    'VAI_المشاركة_والمساءلة_Actual_Source':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Actual_Formula':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Actual_Logic':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Actual_Comments':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Weight':'FLOAT',
    'VAI_المشاركة_والمساءلة_Weight_Formula':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Weight_Logic':'VARCHAR',
    'VAI_المشاركة_والمساءلة_Weight_Comments':'VARCHAR',
    'OCI_الجريمة_المنظمة_Actual':'FLOAT',
    'OCI_الجريمة_المنظمة_Actual_Source':'VARCHAR',
    'OCI_الجريمة_المنظمة_Actual_Formula':'VARCHAR',
    'OCI_الجريمة_المنظمة_Actual_Logic':'VARCHAR',
    'OCI_الجريمة_المنظمة_Actual_Comments':'VARCHAR',
    'OCI_الجريمة_المنظمة_Weight':'FLOAT',
    'OCI_الجريمة_المنظمة_Weight_Formula':'VARCHAR',
    'OCI_الجريمة_المنظمة_Weight_Logic':'VARCHAR',
    'OCI_الجريمة_المنظمة_Weight_Comments':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual':'FLOAT',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Source':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Formula':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Logic':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Comments':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight':'FLOAT',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Formula':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Logic':'VARCHAR',
    'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Comments':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual':'FLOAT',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Source':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Formula':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Logic':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Comments':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight':'FLOAT',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Formula':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Logic':'VARCHAR',
    'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Comments':'VARCHAR',
    'DI_الديمقراطية_Actual':'FLOAT',
    'DI_الديمقراطية_Actual_Source':'VARCHAR',
    'DI_الديمقراطية_Actual_Formula':'VARCHAR',
    'DI_الديمقراطية_Actual_Logic':'VARCHAR',
    'DI_الديمقراطية_Actual_Comments':'VARCHAR',
    'DI_الديمقراطية_Weight':'FLOAT',
    'DI_الديمقراطية_Weight_Formula':'VARCHAR',
    'DI_الديمقراطية_Weight_Logic':'VARCHAR',
    'DI_الديمقراطية_Weight_Comments':'VARCHAR',
    'النتيجة':'VARCHAR', 
    'التوصية':'VARCHAR', 
    'فيديو':'VARCHAR',
    'القطاع_الرئيسي':'VARCHAR', 
    'القطاع_الفرعي':'VARCHAR', 
    'متاح':'INT'}
    
    # Convert the DataFrame columns to the expected data types
    for column, expected_type in expected_data_types.items():
        if column in data.columns:
            if expected_type == 'VARCHAR':
                try:
                    data[column].iloc[-1] = int(data[column].iloc[-1])
                except:
                    pass
                if type(data[column].iloc[-1]) == int:
                    err = f"الرجاء ادخاء المعلومات بصيغة كلمات في {column}"
                    st.error(err)
                    raise 'Stop'
                else:
                    data[column].iloc[-1] = str(data[column].iloc[-1])
                    if len(data[column].iloc[-1]) > 10000:
                        err = f"المعلومات التي ادخلتها طويلة في {column}"
                        st.error(err)
                        raise 'Stop'
                    
            elif expected_type == 'INT':
                try:
                    data[column].iloc[-1] = int(data[column].iloc[-1])
                except Exception as e:
                    err = f"الرجاء ادخاء المعلومات بصيغة ارقام صحيحة في {column}"
                    st.error(err)
                    raise 'Stop'
            elif expected_type == 'FLOAT':
                try:
                    data[column].iloc[-1] = float(data[column].iloc[-1])
                except Exception as e:
                    err = f"الرجاء ادخاء المعلومات بصيغة ارقام عشرية في {column}"
                    st.error(err)
                    raise 'Stop'

    return data, table_name, expected_dtypes


def update_data_in_db_en(data_en, table_name_en):
    expected_dtypes_en = {
    'country':sqlalchemy.types.VARCHAR(200),
    'capital':sqlalchemy.types.VARCHAR(200),
    'currency':sqlalchemy.types.VARCHAR(200),
    'official_language':sqlalchemy.types.VARCHAR(200),
    'population':sqlalchemy.types.INTEGER,
    'population_Source':sqlalchemy.types.TEXT,
    'population_Logic':sqlalchemy.types.TEXT,
    'population_Comments':sqlalchemy.types.TEXT,
    'population_growth_rate%':sqlalchemy.types.Float,
    'population_growth_rate%_Source':sqlalchemy.types.TEXT,
    'population_growth_rate%_Logic':sqlalchemy.types.TEXT,
    'population_growth_rate%_Comments':sqlalchemy.types.TEXT,
    'life_expectancy_male':sqlalchemy.types.Float,
    'life_expectancy_male_Source':sqlalchemy.types.TEXT,
    'life_expectancy_male_Logic':sqlalchemy.types.TEXT,
    'life_expectancy_male_Comments':sqlalchemy.types.TEXT,
    'life_expectancy_female':sqlalchemy.types.Float,
    'life_expectancy_female_Source':sqlalchemy.types.TEXT,
    'life_expectancy_female_Logic':sqlalchemy.types.TEXT,
    'life_expectancy_female_Comments':sqlalchemy.types.TEXT,
    'unemployment_rate%':sqlalchemy.types.Float,
    'unemployment_rate%_Source':sqlalchemy.types.TEXT,
    'unemployment_rate%_Logic':sqlalchemy.types.TEXT,
    'unemployment_rate%_Comments':sqlalchemy.types.TEXT,
    'minimum_wage_dollar/month':sqlalchemy.types.Float,
    'minimum_wage_dollar/month_Source':sqlalchemy.types.TEXT,
    'minimum_wage_dollar/month_Logic':sqlalchemy.types.TEXT,
    'minimum_wage_dollar/month_Comments':sqlalchemy.types.TEXT,
    'population_below_national_poverty_line%':sqlalchemy.types.Float,
    'population_below_national_poverty_line%_Source':sqlalchemy.types.TEXT,
    'population_below_national_poverty_line%_Logic':sqlalchemy.types.TEXT,
    'population_below_national_poverty_line%_Comments':sqlalchemy.types.TEXT,
    'median_household_income':sqlalchemy.types.Float,
    'median_household_income_Source':sqlalchemy.types.TEXT,
    'median_household_income_Logic':sqlalchemy.types.TEXT,
    'median_household_income_Comments':sqlalchemy.types.TEXT,
    'gross_domestic_product_GDP_billion_dollar':sqlalchemy.types.Float,
    'gross_domestic_product_GDP_billion_dollar_Source':sqlalchemy.types.TEXT,
    'gross_domestic_product_GDP_billion_dollar_Logic':sqlalchemy.types.TEXT,
    'gross_domestic_product_GDP_billion_dollar_Comments':sqlalchemy.types.TEXT,
    'GDP_per_capita/yearly':sqlalchemy.types.Float,
    'GDP_per_capita/yearly_Source':sqlalchemy.types.TEXT,
    'GDP_per_capita/yearly_Logic':sqlalchemy.types.TEXT,
    'GDP_per_capita/yearly_Comments':sqlalchemy.types.TEXT,
    'average_per_capita_income_dollar/yearly':sqlalchemy.types.Float,
    'average_per_capita_income_dollar/yearly_Source':sqlalchemy.types.TEXT,
    'average_per_capita_income_dollar/yearly_Logic':sqlalchemy.types.TEXT,
    'average_per_capita_income_dollar/yearly_Comments':sqlalchemy.types.TEXT,
    'currency_exchange_rate_against_dollar':sqlalchemy.types.Float,
    'currency_exchange_rate_against_dollar_Source':sqlalchemy.types.TEXT,
    'currency_exchange_rate_against_dollar_Logic':sqlalchemy.types.TEXT,
    'currency_exchange_rate_against_dollar_Comments':sqlalchemy.types.TEXT,
    'GDP_growth_rate%':sqlalchemy.types.Float,
    'GDP_growth_rate%_Source':sqlalchemy.types.TEXT,
    'GDP_growth_rate%_Logic':sqlalchemy.types.TEXT,
    'GDP_growth_rate%_Comments':sqlalchemy.types.TEXT,
    'gross_national_product_GNP_billion_dollar':sqlalchemy.types.Float,
    'gross_national_product_GNP_billion_dollar_Source':sqlalchemy.types.TEXT,
    'gross_national_product_GNP_billion_dollar_Logic':sqlalchemy.types.TEXT,
    'gross_national_product_GNP_billion_dollar_Comments':sqlalchemy.types.TEXT,
    'state_general_budget_size_Expenditures_million_dollar':sqlalchemy.types.Float,
    'state_general_budget_size_Expenditures_million_Source':sqlalchemy.types.TEXT,
    'state_general_budget_size_Expenditures_million_Logic':sqlalchemy.types.TEXT,
    'state_general_budget_size_Expenditures_million_Comments':sqlalchemy.types.TEXT,
    'general_budget_percent_of_GDP%':sqlalchemy.types.Float,
    'general_budget_percent_of_GDP%_Source':sqlalchemy.types.TEXT,
    'general_budget_percent_of_GDP%_Logic':sqlalchemy.types.TEXT,
    'general_budget_percent_of_GDP%_Comments':sqlalchemy.types.TEXT,
    'general_budget_fiscal_year':sqlalchemy.types.Float,
    'general_budget_fiscal_year_Source':sqlalchemy.types.TEXT,
    'general_budget_fiscal_year_Logic':sqlalchemy.types.TEXT,
    'general_budget_fiscal_year_Comments':sqlalchemy.types.TEXT,
    'total_general_budget_revenues_million_dollar':sqlalchemy.types.Float,
    'total_general_budget_revenues_million_dollar_Source':sqlalchemy.types.TEXT,
    'total_general_budget_revenues_million_dollar_Logic':sqlalchemy.types.TEXT,
    'total_general_budget_revenues_million_dollar_Comments':sqlalchemy.types.TEXT,
    'total_budget_deficit_general_budget_after_grants_million_dollar':sqlalchemy.types.Float,
    'total_budget_deficit_general_budget_after_grants_Source':sqlalchemy.types.TEXT,
    'total_budget_deficit_general_budget_after_grants_million_Logic':sqlalchemy.types.TEXT,
    'total_budget_deficit_general_budget_after_grants_M_Comments':sqlalchemy.types.TEXT,
    'public_debt_to_GDP_ratio%':sqlalchemy.types.Float,
    'public_debt_to_GDP_ratio%_Source':sqlalchemy.types.TEXT,
    'public_debt_to_GDP_ratio%_Logic':sqlalchemy.types.TEXT,
    'public_debt_to_GDP_ratio%_Comments':sqlalchemy.types.TEXT,
    'inflation_rate%':sqlalchemy.types.Float,
    'inflation_rate%_Source':sqlalchemy.types.TEXT,
    'inflation_rate%_Logic':sqlalchemy.types.TEXT,
    'inflation_rate%_Comments':sqlalchemy.types.TEXT,
    'total_budget_deficit_percentage_of_GDP%':sqlalchemy.types.Float,
    'total_budget_deficit_percentage_of_GDP%_Source':sqlalchemy.types.TEXT,
    'total_budget_deficit_percentage_of_GDP%_Logic':sqlalchemy.types.TEXT,
    'total_budget_deficit_percentage_of_GDP%_Comments':sqlalchemy.types.TEXT,
    'external_debt_to_GDP_ratio%':sqlalchemy.types.Float,
    'external_debt_to_GDP_ratio%_Source':sqlalchemy.types.TEXT,
    'external_debt_to_GDP_ratio%_Logic':sqlalchemy.types.TEXT,
    'external_debt_to_GDP_ratio%_Comments':sqlalchemy.types.TEXT,
    'trade_balance_million_dollar':sqlalchemy.types.Float,
    'trade_balance_million_dollar_Source':sqlalchemy.types.TEXT,
    'trade_balance_million_dollar_Logic':sqlalchemy.types.TEXT,
    'trade_balance_million_dollar_Comments':sqlalchemy.types.TEXT,
    'value_of_imports_million_dollar':sqlalchemy.types.Float,
    'value_of_imports_million_dollar_Source':sqlalchemy.types.TEXT,
    'value_of_imports_million_dollar_Logic':sqlalchemy.types.TEXT,
    'value_of_imports_million_dollar_Comments':sqlalchemy.types.TEXT,
    'value_of_exports_million_dollar':sqlalchemy.types.Float,
    'value_of_exports_million_dollar_Source':sqlalchemy.types.TEXT,
    'value_of_exports_million_dollar_Logic':sqlalchemy.types.TEXT,
    'value_of_exports_million_dollar_Comments':sqlalchemy.types.TEXT,
    'balance_of_payments_million_dollar':sqlalchemy.types.Float,
    'balance_of_payments_million_dollar_Source':sqlalchemy.types.TEXT,
    'balance_of_payments_million_dollar_Logic':sqlalchemy.types.TEXT,
    'balance_of_payments_million_dollar_Comments':sqlalchemy.types.TEXT,
    'balance_of_payments_to_GDP%':sqlalchemy.types.Float,
    'balance_of_payments_to_GDP%_Source':sqlalchemy.types.TEXT,
    'balance_of_payments_to_GDP%_Logic':sqlalchemy.types.TEXT,
    'balance_of_payments_to_GDP%_Comments':sqlalchemy.types.TEXT,
    'foreign_direct_investment_million_dollar':sqlalchemy.types.Float,
    'foreign_direct_investment_million_dollar_Source':sqlalchemy.types.TEXT,
    'foreign_direct_investment_million_dollar_Logic':sqlalchemy.types.TEXT,
    'foreign_direct_investment_million_dollar_Comments':sqlalchemy.types.TEXT,
    'available_investment_opportunities_announced_by_state':sqlalchemy.types.TEXT,
    'available_investment_opp_announced_by_state_Source':sqlalchemy.types.TEXT,
    'available_investment_opp_announced_by_state_Logic':sqlalchemy.types.TEXT,
    'available_investment_opp_announced_by_state_Comments':sqlalchemy.types.TEXT,
    'available_investment_opportunities_by_specialized_reports':sqlalchemy.types.TEXT,
    'available_investment_opportunities_specialized_reports_Source':sqlalchemy.types.TEXT,
    'available_investment_opp_by_specialized_reports_Logic':sqlalchemy.types.TEXT,
    'available_investment_opp_by_specialized_reports_Comments':sqlalchemy.types.TEXT,
    'foreign_exchange_reserves_billion_dollar':sqlalchemy.types.Float,
    'foreign_exchange_reserves_billion_dollar_Source':sqlalchemy.types.TEXT,
    'foreign_exchange_reserves_billion_dollar_Logic':sqlalchemy.types.TEXT,
    'foreign_exchange_reserves_billion_dollar_Comments':sqlalchemy.types.TEXT,
    'interest_rate_on_deposits%':sqlalchemy.types.Float,
    'interest_rate_on_deposits%_Source':sqlalchemy.types.TEXT,
    'interest_rate_on_deposits%_Logic':sqlalchemy.types.TEXT,
    'interest_rate_on_deposits%_Comments':sqlalchemy.types.TEXT,
    'Interest_rate_on_credit%':sqlalchemy.types.Float,
    'Interest_rate_on_credit%_Source':sqlalchemy.types.TEXT,
    'Interest_rate_on_credit%_Logic':sqlalchemy.types.TEXT,
    'Interest_rate_on_credit%_Comments':sqlalchemy.types.TEXT,
    'interest_rate_of_licensed_banks/overdraft%':sqlalchemy.types.Float,
    'interest_rate_of_licensed_banks/overdraft%_Source':sqlalchemy.types.TEXT,
    'interest_rate_of_licensed_banks/overdraft%_Logic':sqlalchemy.types.TEXT,
    'interest_rate_of_licensed_banks/overdraft%_Comments':sqlalchemy.types.TEXT,
    'central_bank_general_budget_million_dollar':sqlalchemy.types.Float,
    'central_bank_general_budget_million_dollar_Source':sqlalchemy.types.TEXT,
    'central_bank_general_budget_million_dollar_Logic':sqlalchemy.types.TEXT,
    'central_bank_general_budget_million_dollar_Comments':sqlalchemy.types.TEXT,
    'sales_tax_rate%':sqlalchemy.types.Float,
    'sales_tax_rate%_Source':sqlalchemy.types.TEXT,
    'sales_tax_rate%_Logic':sqlalchemy.types.TEXT,
    'sales_tax_rate%_Comments':sqlalchemy.types.TEXT,
    'income_tax_rate_per_individual%':sqlalchemy.types.Float,
    'income_tax_rate_per_individual%_Source':sqlalchemy.types.TEXT,
    'income_tax_rate_per_individual%_Logic':sqlalchemy.types.TEXT,
    'income_tax_rate_per_individual%_Comments':sqlalchemy.types.TEXT,
    'corporate_income_tax_rate%':sqlalchemy.types.Float,
    'corporate_income_tax_rate%_Source':sqlalchemy.types.TEXT,
    'corporate_income_tax_rate%_Logic':sqlalchemy.types.TEXT,
    'corporate_income_tax_rate%_Comments':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit%':sqlalchemy.types.Float,
    'profit_tax_percent_of_business_profit%_Source':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit%_Logic':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit%_Comments':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit_banks_sector%':sqlalchemy.types.Float,
    'profit_tax_percent_of_business_profit_banks_sector%__Source':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit_banks_sector%_Logic':sqlalchemy.types.TEXT,
    'profit_tax_percent_of_business_profit_banks_sector%_Comments':sqlalchemy.types.TEXT,
    'corruption_index':sqlalchemy.types.Float,
    'corruption_index_Source':sqlalchemy.types.TEXT,
    'corruption_index_Logic':sqlalchemy.types.TEXT,
    'corruption_index_Comments':sqlalchemy.types.TEXT,
    'global_ranking_on_corruption_index':sqlalchemy.types.Float,
    'global_ranking_on_corruption_index_Source':sqlalchemy.types.TEXT,
    'global_ranking_on_corruption_index_Logic':sqlalchemy.types.TEXT,
    'global_ranking_on_corruption_index_Comments':sqlalchemy.types.TEXT,
    'ease_of_doing_business_index':sqlalchemy.types.Float,
    'ease_of_doing_business_index_Source':sqlalchemy.types.TEXT,
    'ease_of_doing_business_index_Logic':sqlalchemy.types.TEXT,
    'ease_of_doing_business_index_Comments':sqlalchemy.types.TEXT,
    'new_business_density':sqlalchemy.types.Float,
    'new_business_density_Source':sqlalchemy.types.TEXT,
    'new_business_density_Logic':sqlalchemy.types.TEXT,
    'new_business_density_Comments':sqlalchemy.types.TEXT,
    'credit_rating_acoording_to_S&P_index':sqlalchemy.types.VARCHAR(200),
    'credit_rating_acoording_to_S&P_index_Source':sqlalchemy.types.TEXT,
    'credit_rating_acoording_to_S&P_index_Logic':sqlalchemy.types.TEXT,
    'credit_rating_acoording_to_S&P_index_Comments':sqlalchemy.types.TEXT,
    "credit_rating_according_to_Moody's":sqlalchemy.types.VARCHAR(200),
    "credit_rating_according_to_Moody's_Source":sqlalchemy.types.TEXT,
    "credit_rating_according_to_Moody's_Logic":sqlalchemy.types.TEXT,
    "credit_rating_according_to_Moody's_Comments":sqlalchemy.types.TEXT,
    'credit_rating_according_to_Fitch':sqlalchemy.types.VARCHAR(200),
    'credit_rating_according_to_Fitch_Source':sqlalchemy.types.TEXT,
    'credit_rating_according_to_Fitch_Logic':sqlalchemy.types.TEXT,
    'credit_rating_according_to_Fitch_Comments':sqlalchemy.types.TEXT,
    'top_exports':sqlalchemy.types.TEXT,
    'top_exports_Source':sqlalchemy.types.TEXT,
    'top_exports_Logic':sqlalchemy.types.TEXT,
    'top_exports_Comments':sqlalchemy.types.TEXT,
    'top_imports':sqlalchemy.types.TEXT,
    'top_imports_Source':sqlalchemy.types.TEXT,
    'top_imports_Logic':sqlalchemy.types.TEXT,
    'top_imports_Comments':sqlalchemy.types.TEXT,
    'year':sqlalchemy.types.INTEGER,
    'GDP_billion_dollar_actual':sqlalchemy.types.Float,
    'GDP_billion_dollar_actual_Source':sqlalchemy.types.TEXT,
    'GDP_billion_dollar_actual_Formula':sqlalchemy.types.TEXT,
    'GDP_billion_dollar_actual_Logic':sqlalchemy.types.TEXT,
    'GDP_billion_dollar_actual_Comments':sqlalchemy.types.TEXT,
    'GDP_weight':sqlalchemy.types.Float,
    'GDP_weight_Formula':sqlalchemy.types.TEXT,
    'GDP_weight_Logic':sqlalchemy.types.TEXT,
    'GDP_weight_Comments':sqlalchemy.types.TEXT,
    'GDP_Growth%_actual':sqlalchemy.types.Float,
    'GDP_Growth%_actual_Source':sqlalchemy.types.TEXT,
    'GDP_Growth%_actual_Formula':sqlalchemy.types.TEXT,
    'GDP_Growth%_actual_Logic':sqlalchemy.types.TEXT,
    'GDP_Growth%_actual_Comments':sqlalchemy.types.TEXT,
    'GDP_Growth_weight':sqlalchemy.types.Float,
    'GDP_Growth_weight_Formula':sqlalchemy.types.TEXT,
    'GDP_Growth_weight_Logic':sqlalchemy.types.TEXT,
    'GDP_Growth_weight_Comments':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth%_actual':sqlalchemy.types.Float,
    'Consumption_expenditure_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth_weight':sqlalchemy.types.Float,
    'Consumption_expenditure_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Consumption_expenditure_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Investment_growth%_actual':sqlalchemy.types.Float,
    'Investment_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Investment_growth_weight':sqlalchemy.types.Float,
    'Investment_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Investment_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Investment_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Government_expenditure_growth%_actual':sqlalchemy.types.Float,
    'Government_expenditure_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Government_expenditure_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Government_expenditure_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Government_expenditure_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Government_expenditure_growth_weight':sqlalchemy.types.Float,
    'Government_expenditure_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Government_expenditure_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Government_expenditure_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit%_actual':sqlalchemy.types.Float,
    'Government_fiscal_deficit%_actual_Source':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit%_actual_Formula':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit%_actual_Logic':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit%_actual_Comments':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit_weight':sqlalchemy.types.Float,
    'Government_fiscal_deficit_weight_Formula':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit_weight_Logic':sqlalchemy.types.TEXT,
    'Government_fiscal_deficit_weight_Comments':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_actual':sqlalchemy.types.Float,
    'Government_debt_(%GDP)_actual_Source':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_actual_Formula':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_actual_Logic':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_actual_Comments':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_weight':sqlalchemy.types.Float,
    'Government_debt_(%GDP)_weight_Formula':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_weight_Logic':sqlalchemy.types.TEXT,
    'Government_debt_(%GDP)_weight_Comments':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual':sqlalchemy.types.Float,
    'Labor_force_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight':sqlalchemy.types.Float,
    'Labor_force_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth%_actual':sqlalchemy.types.Float,
    'Private_sector_debt_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth_weight':sqlalchemy.types.Float,
    'Private_sector_debt_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Private_sector_debt_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Exports_growth%_actual':sqlalchemy.types.Float,
    'Exports_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Exports_growth_weight':sqlalchemy.types.Float,
    'Exports_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Exports_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Exports_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Imports_growth%_actual':sqlalchemy.types.Float,
    'Imports_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Imports_growth_weight':sqlalchemy.types.Float,
    'Imports_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Imports_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Imports_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Currency_stability_actual':sqlalchemy.types.VARCHAR(200),
    'Currency_stability_actual_Source':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Formula':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Logic':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Comments':sqlalchemy.types.TEXT,
    'Currency_stability_weight':sqlalchemy.types.Float,
    'Currency_stability_weight_Formula':sqlalchemy.types.TEXT,
    'Currency_stability_weight_Logic':sqlalchemy.types.TEXT,
    'Currency_stability_weight_Comments':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_actual':sqlalchemy.types.Float,
    'Gross_capital_formation_(GDP%)_actual_Source':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_actual_Formula':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_actual_Logic':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_actual_Comments':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_weight':sqlalchemy.types.Float,
    'Gross_capital_formation_(GDP%)_weight_Formula':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_weight_Logic':sqlalchemy.types.TEXT,
    'Gross_capital_formation_(GDP%)_weight_Comments':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_actual':sqlalchemy.types.Float,
    'foreign_direct_investment_FDI(GDP%)_actual_Source':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_actual_Formula':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_actual_Logic':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_actual_Comments':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_weight':sqlalchemy.types.Float,
    'foreign_direct_investment_FDI(GDP%)_weight_Formula':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_weight_Logic':sqlalchemy.types.TEXT,
    'foreign_direct_investment_FDI(GDP%)_weight_Comments':sqlalchemy.types.TEXT,
    'Productivity_improvement%_actual':sqlalchemy.types.Float,
    'Productivity_improvement%_actual_Source':sqlalchemy.types.TEXT,
    'Productivity_improvement%_actual_Formula':sqlalchemy.types.TEXT,
    'Productivity_improvement%_actual_Logic':sqlalchemy.types.TEXT,
    'Productivity_improvement%_actual_Comments':sqlalchemy.types.TEXT,
    'Productivity_improvement_weight':sqlalchemy.types.Float,
    'Productivity_improvement_weight_Formula':sqlalchemy.types.TEXT,
    'Productivity_improvement_weight_Logic':sqlalchemy.types.TEXT,
    'Productivity_improvement_weight_Comments':sqlalchemy.types.TEXT,
    'TOTAL':sqlalchemy.types.Float,
    'TOTAL_Formula':sqlalchemy.types.TEXT,
    'TOTAL_Logic':sqlalchemy.types.TEXT,
    'TOTAL_Comments':sqlalchemy.types.TEXT,
    'GDP_Revenues':sqlalchemy.types.TEXT,
    'Budget_Revenues':sqlalchemy.types.TEXT,
    'Budget_Expenses':sqlalchemy.types.TEXT,
    'GDP_Revenues_Sources':sqlalchemy.types.TEXT,
    'GDP_Revenues_Logic':sqlalchemy.types.TEXT,
    'GDP_Revenues_Comments':sqlalchemy.types.TEXT,
    'Budget_Revenues_Sources':sqlalchemy.types.TEXT,
    'Budget_Revenues_Logic':sqlalchemy.types.TEXT,
    'Budget_Revenues_Comments':sqlalchemy.types.TEXT,
    'Budget_Expenses_Sources':sqlalchemy.types.TEXT,
    'Budget_Expenses_Logic':sqlalchemy.types.TEXT,
    'Budget_Expenses_Comments':sqlalchemy.types.TEXT,
    'Investment_GDP%_actual':sqlalchemy.types.Float,
    'Investment_GDP%_actual_Source':sqlalchemy.types.TEXT,
    'Investment_GDP%_actual_Formula':sqlalchemy.types.TEXT,
    'Investment_GDP%_actual_Logic':sqlalchemy.types.TEXT,
    'Investment_GDP%_actual_Comments':sqlalchemy.types.TEXT,
    'Investment_GDP%_weight':sqlalchemy.types.Float,
    'Investment_GDP%_weight_Formula':sqlalchemy.types.TEXT,
    'Investment_GDP%_weight_Logic':sqlalchemy.types.TEXT,
    'Investment_GDP%_weight_Comments':sqlalchemy.types.TEXT,
    'Investment_growth%_actual':sqlalchemy.types.Float,
    'Investment_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Investment_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Investment_growth_weight':sqlalchemy.types.Float,
    'Investment_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Investment_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Investment_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy%_actual':sqlalchemy.types.Float,
    'Innovation(R&D)_economy%_actual_Source':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy%_actual_Formula':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy%_actual_Logic':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy%_actual_Comments':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy_weight':sqlalchemy.types.Float,
    'Innovation(R&D)_economy_weight_Formula':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy_weight_Logic':sqlalchemy.types.TEXT,
    'Innovation(R&D)_economy_weight_Comments':sqlalchemy.types.TEXT,
    'Interest_rates%_actual':sqlalchemy.types.Float,
    'Interest_rates%_actual_Source':sqlalchemy.types.TEXT,
    'Interest_rates%_actual_Formula':sqlalchemy.types.TEXT,
    'Interest_rates%_actual_Logic':sqlalchemy.types.TEXT,
    'Interest_rates%_actual_Comments':sqlalchemy.types.TEXT,
    'Interest_rates_weight':sqlalchemy.types.Float,
    'Interest_rates_weight_Formula':sqlalchemy.types.TEXT,
    'Interest_rates_weight_Logic':sqlalchemy.types.TEXT,
    'Interest_rates_weight_Comments':sqlalchemy.types.TEXT,
    'Exports_growth%_actual':sqlalchemy.types.Float,
    'Exports_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Population_growth%_actual':sqlalchemy.types.Float,
    'Population_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Population_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Population_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Population_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Population_growth_weight':sqlalchemy.types.Float,
    'Population_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Population_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Population_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual':sqlalchemy.types.Float,
    'Labor_force_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Labor_force_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight':sqlalchemy.types.Float,
    'Labor_force_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Labor_force_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Saving_rate%_actual':sqlalchemy.types.Float,
    'Saving_rate%_actual_Source':sqlalchemy.types.TEXT,
    'Saving_rate%_actual_Formula':sqlalchemy.types.TEXT,
    'Saving_rate%_actual_Logic':sqlalchemy.types.TEXT,
    'Saving_rate%_actual_Comments':sqlalchemy.types.TEXT,
    'Saving_rate_weight':sqlalchemy.types.Float,
    'Saving_rate_weight_Formula':sqlalchemy.types.TEXT,
    'Saving_rate_weight_Logic':sqlalchemy.types.TEXT,
    'Saving_rate_weight_Comments':sqlalchemy.types.TEXT,
    'Inflation_rate%_actual':sqlalchemy.types.Float,
    'Inflation_rate%_actual_Source':sqlalchemy.types.TEXT,
    'Inflation_rate%_actual_Formula':sqlalchemy.types.TEXT,
    'Inflation_rate%_actual_Logic':sqlalchemy.types.TEXT,
    'Inflation_rate%_actual_Comments':sqlalchemy.types.TEXT,
    'Inflation_rate_weight':sqlalchemy.types.Float,
    'Inflation_rate_weight_Formula':sqlalchemy.types.TEXT,
    'Inflation_rate_weight_Logic':sqlalchemy.types.TEXT,
    'Inflation_rate_weight_Comments':sqlalchemy.types.TEXT,
    'Currency_stability_actual':sqlalchemy.types.VARCHAR(200),
    'Currency_stability_actual_Source':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Formula':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Logic':sqlalchemy.types.TEXT,
    'Currency_stability_actual_Comments':sqlalchemy.types.TEXT,
    'Currency_stability_weight':sqlalchemy.types.Float,
    'Currency_stability_weight_Formula':sqlalchemy.types.TEXT,
    'Currency_stability_weight_Logic':sqlalchemy.types.TEXT,
    'Currency_stability_weight_Comments':sqlalchemy.types.TEXT,
    'Central_bank_independence_actual':sqlalchemy.types.VARCHAR(200),
    'Central_bank_independence_actual_Source':sqlalchemy.types.TEXT,
    'Central_bank_independence_actual_Formula':sqlalchemy.types.TEXT,
    'Central_bank_independence_actual_Logic':sqlalchemy.types.TEXT,
    'Central_bank_independence_actual_Comments':sqlalchemy.types.TEXT,
    'Central_bank_independence_weight':sqlalchemy.types.Float,
    'Central_bank_independence_weight_Formula':sqlalchemy.types.TEXT,
    'Central_bank_independence_weight_Logic':sqlalchemy.types.TEXT,
    'Central_bank_independence_weight_Comments':sqlalchemy.types.TEXT,
    'Exports_growth%_actual':sqlalchemy.types.Float,
    'Exports_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Exports_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Exports_growth_weight':sqlalchemy.types.Float,
    'Exports_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Exports_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Exports_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Imports_growth%_actual':sqlalchemy.types.Float,
    'Imports_growth%_actual_Source':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Formula':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Logic':sqlalchemy.types.TEXT,
    'Imports_growth%_actual_Comments':sqlalchemy.types.TEXT,
    'Imports_growth_weight':sqlalchemy.types.Float,
    'Imports_growth_weight_Formula':sqlalchemy.types.TEXT,
    'Imports_growth_weight_Logic':sqlalchemy.types.TEXT,
    'Imports_growth_weight_Comments':sqlalchemy.types.TEXT,
    'Trade_balance_billion_dollar_actual':sqlalchemy.types.Float,
    'Trade_balance_billion_dollar_actual_Source':sqlalchemy.types.TEXT,
    'Trade_balance_billion_dollar_actual_Formula':sqlalchemy.types.TEXT,
    'Trade_balance_billion_dollar_actual_Logic':sqlalchemy.types.TEXT,
    'Trade_balance_billion_dollar_actual_Comments':sqlalchemy.types.TEXT,
    'Trade_balance_weight':sqlalchemy.types.Float,
    'Trade_balance_weight_Formula':sqlalchemy.types.TEXT,
    'Trade_balance_weight_Logic':sqlalchemy.types.TEXT,
    'Trade_balance_weight_Comments':sqlalchemy.types.TEXT,
    'Fiscal_deficit_million_dollar_actual':sqlalchemy.types.Float,
    'Fiscal_deficit_million_dollar_actual_Source':sqlalchemy.types.TEXT,
    'Fiscal_deficit_million_dollar_actual_Formula':sqlalchemy.types.TEXT,
    'Fiscal_deficit_million_dollar_actual_Logic':sqlalchemy.types.TEXT,
    'Fiscal_deficit_million_dollar_actual_Comments':sqlalchemy.types.TEXT,
    'Fiscal_deficit_weight':sqlalchemy.types.Float,
    'Fiscal_deficit_weight_Formula':sqlalchemy.types.TEXT,
    'Fiscal_deficit_weight_Logic':sqlalchemy.types.TEXT,
    'Fiscal_deficit_weight_Comments':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_actual':sqlalchemy.types.Float,
    'External_debt_(GPD%)_actual_Formula':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_actual_Logic':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_actual_Comments':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_actual_Source':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_weight':sqlalchemy.types.Float,
    'External_debt_(GPD%)_weight_Formula':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_weight_Logic':sqlalchemy.types.TEXT,
    'External_debt_(GPD%)_weight_Comments':sqlalchemy.types.TEXT,
    'sector':sqlalchemy.types.VARCHAR(200),
    'subsector':sqlalchemy.types.VARCHAR(200),
    'title':sqlalchemy.types.TEXT,
    'description':sqlalchemy.types.TEXT,
    'approximate_cost':sqlalchemy.types.TEXT,
    'return_on_investment':sqlalchemy.types.TEXT,
    'macroeconomic_stability_actual%':sqlalchemy.types.Float,
    'macroeconomic_stability_actual_Source':sqlalchemy.types.TEXT,
    'macroeconomic_stability_actual%_Formula':sqlalchemy.types.TEXT,
    'macroeconomic_stability_actual%_Logic':sqlalchemy.types.TEXT,
    'macroeconomic_stability_actual%_Comments':sqlalchemy.types.TEXT,
    'macroeconomic_stability_weight':sqlalchemy.types.Float,
    'macroeconomic_stability_weight_Formula':sqlalchemy.types.TEXT,
    'macroeconomic_stability_weight_Logic':sqlalchemy.types.TEXT,
    'macroeconomic_stability_weight_Comments':sqlalchemy.types.TEXT,
    'policy_uncertainty_actual%':sqlalchemy.types.Float,
    'policy_uncertainty_actual_Source':sqlalchemy.types.TEXT,
    'policy_uncertainty_actual%_Formula':sqlalchemy.types.TEXT,
    'policy_uncertainty_actual%_Logic':sqlalchemy.types.TEXT,
    'policy_uncertainty_actual%_Comments':sqlalchemy.types.TEXT,
    'policy_uncertainty_weight':sqlalchemy.types.Float,
    'policy_uncertainty_weight_Formula':sqlalchemy.types.TEXT,
    'policy_uncertainty_weight_Logic':sqlalchemy.types.TEXT,
    'policy_uncertainty_weight_Comments':sqlalchemy.types.TEXT,
    'corruption_actual%':sqlalchemy.types.Float,
    'corruption_actual_Source':sqlalchemy.types.TEXT,
    'corruption_actual%_Formula':sqlalchemy.types.TEXT,
    'corruption_actual%_Logic':sqlalchemy.types.TEXT,
    'corruption_actual%_Comments':sqlalchemy.types.TEXT,
    'corruption_weight':sqlalchemy.types.Float,
    'corruption_weight_Formula':sqlalchemy.types.TEXT,
    'corruption_weight_Logic':sqlalchemy.types.TEXT,
    'corruption_weight_Comments':sqlalchemy.types.TEXT,
    'tax_rates_burden_actual%':sqlalchemy.types.Float,
    'tax_rates_burden_actual_Source':sqlalchemy.types.TEXT,
    'tax_rates_burden_actual%_Formula':sqlalchemy.types.TEXT,
    'tax_rates_burden_actual%_Logic':sqlalchemy.types.TEXT,
    'tax_rates_burden_actual%_Comments':sqlalchemy.types.TEXT,
    'tax_rates_burden_weight':sqlalchemy.types.Float,
    'tax_rates_burden_weight_Formula':sqlalchemy.types.TEXT,
    'tax_rates_burden_weight_Logic':sqlalchemy.types.TEXT,
    'tax_rates_burden_weight_Comments':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_actual%':sqlalchemy.types.Float,
    'cost_access_to_finance_GlobalFinanceIndex_actual_Source':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Formula':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Logic':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Comments':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_weight':sqlalchemy.types.Float,
    'cost_access_to_finance_GlobalFinanceIndex_weight_Formula':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_weight_Logic':sqlalchemy.types.TEXT,
    'cost_access_to_finance_GlobalFinanceIndex_weight_Comments':sqlalchemy.types.TEXT,
    'crime_actual%':sqlalchemy.types.Float,
    'crime_actual_Source':sqlalchemy.types.TEXT,
    'crime_actual%_Formula':sqlalchemy.types.TEXT,
    'crime_actual%_Logic':sqlalchemy.types.TEXT,
    'crime_actual%_Comments':sqlalchemy.types.TEXT,
    'crime_weight':sqlalchemy.types.Float,
    'crime_weight_Formula':sqlalchemy.types.TEXT,
    'crime_weight_Logic':sqlalchemy.types.TEXT,
    'crime_weight_Comments':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_actual%':sqlalchemy.types.Float,
    'regulation_and_tax_administration_actual_Source':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_actual%_Formula':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_actual%_Logic':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_actual%_Comments':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_weight':sqlalchemy.types.Float,
    'regulation_and_tax_administration_weight_Formula':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_weight_Logic':sqlalchemy.types.TEXT,
    'regulation_and_tax_administration_weight_Comments':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_actual%':sqlalchemy.types.Float,
    'skills-based_economy_SBEI_actual_Source':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_actual%_Formula':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_actual%_Logic':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_actual%_Comments':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_weight':sqlalchemy.types.Float,
    'skills-based_economy_SBEI_weight_Formula':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_weight_Logic':sqlalchemy.types.TEXT,
    'skills-based_economy_SBEI_weight_Comments':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_actual%':sqlalchemy.types.Float,
    'quality_of_education_primary_tertiary_actual_Source':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_actual%_Formula':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_actual%_Logic':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_actual%_Comments':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_weight':sqlalchemy.types.Float,
    'quality_of_education_primary_tertiary_weight_Formula':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_weight_Logic':sqlalchemy.types.TEXT,
    'quality_of_education_primary_tertiary_weight_Comments':sqlalchemy.types.TEXT,
    'quality_of_healthcare_actual%':sqlalchemy.types.Float,
    'quality_of_healthcare_actual_Source':sqlalchemy.types.TEXT,
    'quality_of_healthcare_actual%_Formula':sqlalchemy.types.TEXT,
    'quality_of_healthcare_actual%_Logic':sqlalchemy.types.TEXT,
    'quality_of_healthcare_actual%_Comments':sqlalchemy.types.TEXT,
    'quality_of_healthcare_weight':sqlalchemy.types.Float,
    'quality_of_healthcare_weight_Formula':sqlalchemy.types.TEXT,
    'quality_of_healthcare_weight_Logic':sqlalchemy.types.TEXT,
    'quality_of_healthcare_weight_Comments':sqlalchemy.types.TEXT,
    'rule_of_law_actual%':sqlalchemy.types.Float,
    'rule_of_law_actual_Source':sqlalchemy.types.TEXT,
    'rule_of_law_actual%_Formula':sqlalchemy.types.TEXT,
    'rule_of_law_actual%_Logic':sqlalchemy.types.TEXT,
    'rule_of_law_actual%_Comments':sqlalchemy.types.TEXT,
    'rule_of_law_weight':sqlalchemy.types.Float,
    'rule_of_law_weight_Formula':sqlalchemy.types.TEXT,
    'rule_of_law_weight_Logic':sqlalchemy.types.TEXT,
    'rule_of_law_weight_Comments':sqlalchemy.types.TEXT,
    'transportation_actual%':sqlalchemy.types.Float,
    'transportation_actual_Source':sqlalchemy.types.TEXT,
    'transportation_actual%_Formula':sqlalchemy.types.TEXT,
    'transportation_actual%_Logic':sqlalchemy.types.TEXT,
    'transportation_actual%_Comments':sqlalchemy.types.TEXT,
    'transportation_weight':sqlalchemy.types.Float,
    'transportation_weight_Formula':sqlalchemy.types.TEXT,
    'transportation_weight_Logic':sqlalchemy.types.TEXT,
    'transportation_weight_Comments':sqlalchemy.types.TEXT,
    'telecommunication_actual%':sqlalchemy.types.Float,
    'telecommunication_actual_Source':sqlalchemy.types.TEXT,
    'telecommunication_actual%_Formula':sqlalchemy.types.TEXT,
    'telecommunication_actual%_Logic':sqlalchemy.types.TEXT,
    'telecommunication_actual%_Comments':sqlalchemy.types.TEXT,
    'telecommunication_weight':sqlalchemy.types.Float,
    'telecommunication_weight_Formula':sqlalchemy.types.TEXT,
    'telecommunication_weight_Logic':sqlalchemy.types.TEXT,
    'telecommunication_weight_Comments':sqlalchemy.types.TEXT,
    'digitalization_actual%':sqlalchemy.types.Float,
    'digitalization_actual_Source':sqlalchemy.types.TEXT,
    'digitalization_actual%_Formula':sqlalchemy.types.TEXT,
    'digitalization_actual%_Logic':sqlalchemy.types.TEXT,
    'digitalization_actual%_Comments':sqlalchemy.types.TEXT,
    'digitalization_weight':sqlalchemy.types.Float,
    'digitalization_weight_Formula':sqlalchemy.types.TEXT,
    'digitalization_weight_Logic':sqlalchemy.types.TEXT,
    'digitalization_weight_Comments':sqlalchemy.types.TEXT,
    'cost_of_living_actual%':sqlalchemy.types.Float,
    'cost_of_living_actual_Source':sqlalchemy.types.TEXT,
    'cost_of_living_actual%_Formula':sqlalchemy.types.TEXT,
    'cost_of_living_actual%_Logic':sqlalchemy.types.TEXT,
    'cost_of_living_actual%_Comments':sqlalchemy.types.TEXT,
    'cost_of_living_weight':sqlalchemy.types.Float,
    'cost_of_living_weight_Formula':sqlalchemy.types.TEXT,
    'cost_of_living_weight_Logic':sqlalchemy.types.TEXT,
    'cost_of_living_weight_Comments':sqlalchemy.types.TEXT,
    'quality_of_living_actual%':sqlalchemy.types.Float,
    'quality_of_living_actual_Source':sqlalchemy.types.TEXT,
    'quality_of_living_actual%_Formula':sqlalchemy.types.TEXT,
    'quality_of_living_actual%_Logic':sqlalchemy.types.TEXT,
    'quality_of_living_actual%_Comments':sqlalchemy.types.TEXT,
    'quality_of_living_weight':sqlalchemy.types.Float,
    'quality_of_living_weight_Formula':sqlalchemy.types.TEXT,
    'quality_of_living_weight_Logic':sqlalchemy.types.TEXT,
    'quality_of_living_weight_Comments':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Actual':sqlalchemy.types.Float,
    'GPI_Global_Peace_Actual_Source':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Actual_Formula':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Actual_Logic':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Actual_Comments':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Weight':sqlalchemy.types.Float,
    'GPI_Global_Peace_Weight_Formula':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Weight_Logic':sqlalchemy.types.TEXT,
    'GPI_Global_Peace_Weight_Comments':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Actual':sqlalchemy.types.Float,
    'PSI_Political_Stability_Actual_Source':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Actual_Formula':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Actual_Logic':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Actual_Comments':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Weight':sqlalchemy.types.Float,
    'PSI_Political_Stability_Weight_Formula':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Weight_Logic':sqlalchemy.types.TEXT,
    'PSI_Political_Stability_Weight_Comments':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Actual':sqlalchemy.types.Float,
    'CPI_Corruption_Perception_Actual_Source':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Actual_Formula':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Actual_Logic':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Actual_Comments':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Weight':sqlalchemy.types.Float,
    'CPI_Corruption_Perception_Weight_Formula':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Weight_Logic':sqlalchemy.types.TEXT,
    'CPI_Corruption_Perception_Weight_Comments':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Actual':sqlalchemy.types.Float,
    'GTI_Global_Terrorism_Actual_Source':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Actual_Formula':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Actual_Logic':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Actual_Comments':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Weight':sqlalchemy.types.Float,
    'GTI_Global_Terrorism_Weight_Formula':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Weight_Logic':sqlalchemy.types.TEXT,
    'GTI_Global_Terrorism_Weight_Comments':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Actual':sqlalchemy.types.Float,
    'WRI_World_Risk_Actual_Source':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Actual_Formula':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Actual_Logic':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Actual_Comments':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Weight':sqlalchemy.types.Float,
    'WRI_World_Risk_Weight_Formula':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Weight_Logic':sqlalchemy.types.TEXT,
    'WRI_World_Risk_Weight_Comments':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Actual':sqlalchemy.types.Float,
    'HDI_Human_Development_Actual_Source':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Actual_Formula':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Actual_Logic':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Actual_Comments':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Weight':sqlalchemy.types.Float,
    'HDI_Human_Development_Weight_Formula':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Weight_Logic':sqlalchemy.types.TEXT,
    'HDI_Human_Development_Weight_Comments':sqlalchemy.types.TEXT,
    'TI_Transparency_Actual':sqlalchemy.types.Float,
    'TI_Transparency_Actual_Source':sqlalchemy.types.TEXT,
    'TI_Transparency_Actual_Formula':sqlalchemy.types.TEXT,
    'TI_Transparency_Actual_Logic':sqlalchemy.types.TEXT,
    'TI_Transparency_Actual_Comments':sqlalchemy.types.TEXT,
    'TI_Transparency_Weight':sqlalchemy.types.Float,
    'TI_Transparency_Weight_Formula':sqlalchemy.types.TEXT,
    'TI_Transparency_Weight_Logic':sqlalchemy.types.TEXT,
    'TI_Transparency_Weight_Comments':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Actual':sqlalchemy.types.Float,
    'BEI_Business_Enviroment_Actual_Source':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Actual_Formula':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Actual_Logic':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Actual_Comments':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Weight':sqlalchemy.types.Float,
    'BEI_Business_Enviroment_Weight_Formula':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Weight_Logic':sqlalchemy.types.TEXT,
    'BEI_Business_Enviroment_Weight_Comments':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Actual':sqlalchemy.types.Float,
    'WJP_Rule_of_Law_Actual_Source':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Actual_Formula':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Actual_Logic':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Actual_Comments':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Weight':sqlalchemy.types.Float,
    'WJP_Rule_of_Law_Weight_Formula':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Weight_Logic':sqlalchemy.types.TEXT,
    'WJP_Rule_of_Law_Weight_Comments':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Actual':sqlalchemy.types.Float,
    'VAI_Voice_and_Accountability_Actual_Source':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Actual_Formula':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Actual_Logic':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Actual_Comments':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Weight':sqlalchemy.types.Float,
    'VAI_Voice_and_Accountability_Weight_Formula':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Weight_Logic':sqlalchemy.types.TEXT,
    'VAI_Voice_and_Accountability_Weight_Comments':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Actual':sqlalchemy.types.Float,
    'OCI_Organized_Crime_Actual_Source':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Actual_Formula':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Actual_Logic':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Actual_Comments':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Weight':sqlalchemy.types.Float,
    'OCI_Organized_Crime_Weight_Formula':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Weight_Logic':sqlalchemy.types.TEXT,
    'OCI_Organized_Crime_Weight_Comments':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Actual':sqlalchemy.types.Float,
    'FHPRI_Freedom_House_Political_Rights_Actual_Source':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Actual_Formula':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Actual_Logic':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Actual_Comments':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Weight':sqlalchemy.types.Float,
    'FHPRI_Freedom_House_Political_Rights_Weight_Formula':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Weight_Logic':sqlalchemy.types.TEXT,
    'FHPRI_Freedom_House_Political_Rights_Weight_Comments':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Actual':sqlalchemy.types.Float,
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Source':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Formula':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Logic':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Comments':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Weight':sqlalchemy.types.Float,
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Formula':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Logic':sqlalchemy.types.TEXT,
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Comments':sqlalchemy.types.TEXT,
    'DI_Democracy_Actual':sqlalchemy.types.Float,
    'DI_Democracy_Actual_Source':sqlalchemy.types.TEXT,
    'DI_Democracy_Actual_Formula':sqlalchemy.types.TEXT,
    'DI_Democracy_Actual_Logic':sqlalchemy.types.TEXT,
    'DI_Democracy_Actual_Comments':sqlalchemy.types.TEXT,
    'DI_Democracy_Weight':sqlalchemy.types.Float,
    'DI_Democracy_Weight_Formula':sqlalchemy.types.TEXT,
    'DI_Democracy_Weight_Logic':sqlalchemy.types.TEXT,
    'DI_Democracy_Weight_Comments':sqlalchemy.types.TEXT,
    'result':sqlalchemy.types.TEXT, 
    'recommendation':sqlalchemy.types.TEXT, 
    'video':sqlalchemy.types.VARCHAR(3500),
    'main_sector':sqlalchemy.types.VARCHAR(250),
    'subsector':sqlalchemy.types.VARCHAR(250), 
    'available':sqlalchemy.types.INTEGER}

    expected_data_types_en = {
    'country':'VARCHAR',
    'capital':'VARCHAR',
    'currency':'VARCHAR',
    'official_language':'VARCHAR',
    'population':'INT',
    'population_Source':'VARCHAR',
    'population_Logic':'VARCHAR',
    'population_Comments':'VARCHAR',
    'population_growth_rate%':'FLOAT',
    'population_growth_rate%_Source':'VARCHAR',
    'population_growth_rate%_Logic':'VARCHAR',
    'population_growth_rate%_Comments':'VARCHAR',
    'life_expectancy_male':'FLOAT',
    'life_expectancy_male_Source':'VARCHAR',
    'life_expectancy_male_Logic':'VARCHAR',
    'life_expectancy_male_Comments':'VARCHAR',
    'life_expectancy_female':'FLOAT',
    'life_expectancy_female_Source':'VARCHAR',
    'life_expectancy_female_Logic':'VARCHAR',
    'life_expectancy_female_Comments':'VARCHAR',
    'unemployment_rate%':'FLOAT',
    'unemployment_rate%_Source':'VARCHAR',
    'unemployment_rate%_Logic':'VARCHAR',
    'unemployment_rate%_Comments':'VARCHAR',
    'minimum_wage_dollar/month':'FLOAT',
    'minimum_wage_dollar/month_Source':'VARCHAR',
    'minimum_wage_dollar/month_Logic':'VARCHAR',
    'minimum_wage_dollar/month_Comments':'VARCHAR',
    'population_below_national_poverty_line%':'FLOAT',
    'population_below_national_poverty_line%_Source':'VARCHAR',
    'population_below_national_poverty_line%_Logic':'VARCHAR',
    'population_below_national_poverty_line%_Comments':'VARCHAR',
    'median_household_income':'FLOAT',
    'median_household_income_Source':'VARCHAR',
    'median_household_income_Logic':'VARCHAR',
    'median_household_income_Comments':'VARCHAR',
    'gross_domestic_product_GDP_billion_dollar':'FLOAT',
    'gross_domestic_product_GDP_billion_dollar_Source':'VARCHAR',
    'gross_domestic_product_GDP_billion_dollar_Logic':'VARCHAR',
    'gross_domestic_product_GDP_billion_dollar_Comments':'VARCHAR',
    'GDP_per_capita/yearly':'FLOAT',
    'GDP_per_capita/yearly_Source':'VARCHAR',
    'GDP_per_capita/yearly_Logic':'VARCHAR',
    'GDP_per_capita/yearly_Comments':'VARCHAR',
    'average_per_capita_income_dollar/yearly':'FLOAT',
    'average_per_capita_income_dollar/yearly_Source':'VARCHAR',
    'average_per_capita_income_dollar/yearly_Logic':'VARCHAR',
    'average_per_capita_income_dollar/yearly_Comments':'VARCHAR',
    'currency_exchange_rate_against_dollar':'FLOAT',
    'currency_exchange_rate_against_dollar_Source':'VARCHAR',
    'currency_exchange_rate_against_dollar_Logic':'VARCHAR',
    'currency_exchange_rate_against_dollar_Comments':'VARCHAR',
    'GDP_growth_rate%':'FLOAT',
    'GDP_growth_rate%_Source':'VARCHAR',
    'GDP_growth_rate%_Logic':'VARCHAR',
    'GDP_growth_rate%_Comments':'VARCHAR',
    'gross_national_product_GNP_billion_dollar':'FLOAT',
    'gross_national_product_GNP_billion_dollar_Source':'VARCHAR',
    'gross_national_product_GNP_billion_dollar_Logic':'VARCHAR',
    'gross_national_product_GNP_billion_dollar_Comments':'VARCHAR',
    'state_general_budget_size_Expenditures_million_dollar':'FLOAT',
    'state_general_budget_size_Expenditures_million_Source':'VARCHAR',
    'state_general_budget_size_Expenditures_million_Logic':'VARCHAR',
    'state_general_budget_size_Expenditures_million_Comments':'VARCHAR',
    'general_budget_percent_of_GDP%':'FLOAT',
    'general_budget_percent_of_GDP%_Source':'VARCHAR',
    'general_budget_percent_of_GDP%_Logic':'VARCHAR',
    'general_budget_percent_of_GDP%_Comments':'VARCHAR',
    'general_budget_fiscal_year':'FLOAT',
    'general_budget_fiscal_year_Source':'VARCHAR',
    'general_budget_fiscal_year_Logic':'VARCHAR',
    'general_budget_fiscal_year_Comments':'VARCHAR',
    'total_general_budget_revenues_million_dollar':'FLOAT',
    'total_general_budget_revenues_million_dollar_Source':'VARCHAR',
    'total_general_budget_revenues_million_dollar_Logic':'VARCHAR',
    'total_general_budget_revenues_million_dollar_Comments':'VARCHAR',
    'total_budget_deficit_general_budget_after_grants_million_dollar':'FLOAT',
    'total_budget_deficit_general_budget_after_grants_Source':'VARCHAR',
    'total_budget_deficit_general_budget_after_grants_million_Logic':'VARCHAR',
    'total_budget_deficit_general_budget_after_grants_M_Comments':'VARCHAR',
    'public_debt_to_GDP_ratio%':'FLOAT',
    'public_debt_to_GDP_ratio%_Source':'VARCHAR',
    'public_debt_to_GDP_ratio%_Logic':'VARCHAR',
    'public_debt_to_GDP_ratio%_Comments':'VARCHAR',
    'inflation_rate%':'FLOAT',
    'inflation_rate%_Source':'VARCHAR',
    'inflation_rate%_Logic':'VARCHAR',
    'inflation_rate%_Comments':'VARCHAR',
    'total_budget_deficit_percentage_of_GDP%':'FLOAT',
    'total_budget_deficit_percentage_of_GDP%_Source':'VARCHAR',
    'total_budget_deficit_percentage_of_GDP%_Logic':'VARCHAR',
    'total_budget_deficit_percentage_of_GDP%_Comments':'VARCHAR',
    'external_debt_to_GDP_ratio%':'FLOAT',
    'external_debt_to_GDP_ratio%_Source':'VARCHAR',
    'external_debt_to_GDP_ratio%_Logic':'VARCHAR',
    'external_debt_to_GDP_ratio%_Comments':'VARCHAR',
    'trade_balance_million_dollar':'FLOAT',
    'trade_balance_million_dollar_Source':'VARCHAR',
    'trade_balance_million_dollar_Logic':'VARCHAR',
    'trade_balance_million_dollar_Comments':'VARCHAR',
    'value_of_imports_million_dollar':'FLOAT',
    'value_of_imports_million_dollar_Source':'VARCHAR',
    'value_of_imports_million_dollar_Logic':'VARCHAR',
    'value_of_imports_million_dollar_Comments':'VARCHAR',
    'value_of_exports_million_dollar':'FLOAT',
    'value_of_exports_million_dollar_Source':'VARCHAR',
    'value_of_exports_million_dollar_Logic':'VARCHAR',
    'value_of_exports_million_dollar_Comments':'VARCHAR',
    'balance_of_payments_million_dollar':'FLOAT',
    'balance_of_payments_million_dollar_Source':'VARCHAR',
    'balance_of_payments_million_dollar_Logic':'VARCHAR',
    'balance_of_payments_million_dollar_Comments':'VARCHAR',
    'balance_of_payments_to_GDP%':'FLOAT',
    'balance_of_payments_to_GDP%_Source':'VARCHAR',
    'balance_of_payments_to_GDP%_Logic':'VARCHAR',
    'balance_of_payments_to_GDP%_Comments':'VARCHAR',
    'foreign_direct_investment_million_dollar':'FLOAT',
    'foreign_direct_investment_million_dollar_Source':'VARCHAR',
    'foreign_direct_investment_million_dollar_Logic':'VARCHAR',
    'foreign_direct_investment_million_dollar_Comments':'VARCHAR',
    'available_investment_opportunities_announced_by_state':'VARCHAR',
    'available_investment_opp_announced_by_state_Source':'VARCHAR',
    'available_investment_opp_announced_by_state_Logic':'VARCHAR',
    'available_investment_opp_announced_by_state_Comments':'VARCHAR',
    'available_investment_opportunities_by_specialized_reports':'VARCHAR',
    'available_investment_opportunities_specialized_reports_Source':'VARCHAR',
    'available_investment_opp_by_specialized_reports_Logic':'VARCHAR',
    'available_investment_opp_by_specialized_reports_Comments':'VARCHAR',
    'foreign_exchange_reserves_billion_dollar':'FLOAT',
    'foreign_exchange_reserves_billion_dollar_Source':'VARCHAR',
    'foreign_exchange_reserves_billion_dollar_Logic':'VARCHAR',
    'foreign_exchange_reserves_billion_dollar_Comments':'VARCHAR',
    'interest_rate_on_deposits%':'FLOAT',
    'interest_rate_on_deposits%_Source':'VARCHAR',
    'interest_rate_on_deposits%_Logic':'VARCHAR',
    'interest_rate_on_deposits%_Comments':'VARCHAR',
    'Interest_rate_on_credit%':'FLOAT',
    'Interest_rate_on_credit%_Source':'VARCHAR',
    'Interest_rate_on_credit%_Logic':'VARCHAR',
    'Interest_rate_on_credit%_Comments':'VARCHAR',
    'interest_rate_of_licensed_banks/overdraft%':'FLOAT',
    'interest_rate_of_licensed_banks/overdraft%_Source':'VARCHAR',
    'interest_rate_of_licensed_banks/overdraft%_Logic':'VARCHAR',
    'interest_rate_of_licensed_banks/overdraft%_Comments':'VARCHAR',
    'central_bank_general_budget_million_dollar':'FLOAT',
    'central_bank_general_budget_million_dollar_Source':'VARCHAR',
    'central_bank_general_budget_million_dollar_Logic':'VARCHAR',
    'central_bank_general_budget_million_dollar_Comments':'VARCHAR',
    'sales_tax_rate%':'FLOAT',
    'sales_tax_rate%_Source':'VARCHAR',
    'sales_tax_rate%_Logic':'VARCHAR',
    'sales_tax_rate%_Comments':'VARCHAR',
    'income_tax_rate_per_individual%':'FLOAT',
    'income_tax_rate_per_individual%_Source':'VARCHAR',
    'income_tax_rate_per_individual%_Logic':'VARCHAR',
    'income_tax_rate_per_individual%_Comments':'VARCHAR',
    'corporate_income_tax_rate%':'FLOAT',
    'corporate_income_tax_rate%_Source':'VARCHAR',
    'corporate_income_tax_rate%_Logic':'VARCHAR',
    'corporate_income_tax_rate%_Comments':'VARCHAR',
    'profit_tax_percent_of_business_profit%':'FLOAT',
    'profit_tax_percent_of_business_profit%_Source':'VARCHAR',
    'profit_tax_percent_of_business_profit%_Logic':'VARCHAR',
    'profit_tax_percent_of_business_profit%_Comments':'VARCHAR',
    'profit_tax_percent_of_business_profit_banks_sector%':'FLOAT',
    'profit_tax_percent_of_business_profit_banks_sector%__Source':'VARCHAR',
    'profit_tax_percent_of_business_profit_banks_sector%_Logic':'VARCHAR',
    'profit_tax_percent_of_business_profit_banks_sector%_Comments':'VARCHAR',
    'corruption_index':'FLOAT',
    'corruption_index_Source':'VARCHAR',
    'corruption_index_Logic':'VARCHAR',
    'corruption_index_Comments':'VARCHAR',
    'global_ranking_on_corruption_index':'FLOAT',
    'global_ranking_on_corruption_index_Source':'VARCHAR',
    'global_ranking_on_corruption_index_Logic':'VARCHAR',
    'global_ranking_on_corruption_index_Comments':'VARCHAR',
    'ease_of_doing_business_index':'FLOAT',
    'ease_of_doing_business_index_Source':'VARCHAR',
    'ease_of_doing_business_index_Logic':'VARCHAR',
    'ease_of_doing_business_index_Comments':'VARCHAR',
    'new_business_density':'FLOAT',
    'new_business_density_Source':'VARCHAR',
    'new_business_density_Logic':'VARCHAR',
    'new_business_density_Comments':'VARCHAR',
    'credit_rating_acoording_to_S&P_index':'VARCHAR',
    'credit_rating_acoording_to_S&P_index_Source':'VARCHAR',
    'credit_rating_acoording_to_S&P_index_Logic':'VARCHAR',
    'credit_rating_acoording_to_S&P_index_Comments':'VARCHAR',
    "credit_rating_according_to_Moody's":'VARCHAR',
    "credit_rating_according_to_Moody's_Source":'VARCHAR',
    "credit_rating_according_to_Moody's_Logic":'VARCHAR',
    "credit_rating_according_to_Moody's_Comments":'VARCHAR',
    'credit_rating_according_to_Fitch':'VARCHAR',
    'credit_rating_according_to_Fitch_Source':'VARCHAR',
    'credit_rating_according_to_Fitch_Logic':'VARCHAR',
    'credit_rating_according_to_Fitch_Comments':'VARCHAR',
    'top_exports':'VARCHAR',
    'top_exports_Source':'VARCHAR',
    'top_exports_Logic':'VARCHAR',
    'top_exports_Comments':'VARCHAR',
    'top_imports':'VARCHAR',
    'top_imports_Source':'VARCHAR',
    'top_imports_Logic':'VARCHAR',
    'top_imports_Comments':'VARCHAR',
    'year':'INT',
    'GDP_billion_dollar_actual':'FLOAT',
    'GDP_billion_dollar_actual_Source':'VARCHAR',
    'GDP_billion_dollar_actual_Formula':'VARCHAR',
    'GDP_billion_dollar_actual_Logic':'VARCHAR',
    'GDP_billion_dollar_actual_Comments':'VARCHAR',
    'GDP_weight':'FLOAT',
    'GDP_weight_Formula':'VARCHAR',
    'GDP_weight_Logic':'VARCHAR',
    'GDP_weight_Comments':'VARCHAR',
    'GDP_Growth%_actual':'FLOAT',
    'GDP_Growth%_actual_Source':'VARCHAR',
    'GDP_Growth%_actual_Formula':'VARCHAR',
    'GDP_Growth%_actual_Logic':'VARCHAR',
    'GDP_Growth%_actual_Comments':'VARCHAR',
    'GDP_Growth_weight':'FLOAT',
    'GDP_Growth_weight_Formula':'VARCHAR',
    'GDP_Growth_weight_Logic':'VARCHAR',
    'GDP_Growth_weight_Comments':'VARCHAR',
    'Consumption_expenditure_growth%_actual':'FLOAT',
    'Consumption_expenditure_growth%_actual_Source':'VARCHAR',
    'Consumption_expenditure_growth%_actual_Formula':'VARCHAR',
    'Consumption_expenditure_growth%_actual_Logic':'VARCHAR',
    'Consumption_expenditure_growth%_actual_Comments':'VARCHAR',
    'Consumption_expenditure_growth_weight':'FLOAT',
    'Consumption_expenditure_growth_weight_Formula':'VARCHAR',
    'Consumption_expenditure_growth_weight_Logic':'VARCHAR',
    'Consumption_expenditure_growth_weight_Comments':'VARCHAR',
    'Investment_growth%_actual':'FLOAT',
    'Investment_growth%_actual_Source':'VARCHAR',
    'Investment_growth%_actual_Formula':'VARCHAR',
    'Investment_growth%_actual_Logic':'VARCHAR',
    'Investment_growth%_actual_Comments':'VARCHAR',
    'Investment_growth_weight':'FLOAT',
    'Investment_growth_weight_Formula':'VARCHAR',
    'Investment_growth_weight_Logic':'VARCHAR',
    'Investment_growth_weight_Comments':'VARCHAR',
    'Government_expenditure_growth%_actual':'FLOAT',
    'Government_expenditure_growth%_actual_Source':'VARCHAR',
    'Government_expenditure_growth%_actual_Formula':'VARCHAR',
    'Government_expenditure_growth%_actual_Logic':'VARCHAR',
    'Government_expenditure_growth%_actual_Comments':'VARCHAR',
    'Government_expenditure_growth_weight':'FLOAT',
    'Government_expenditure_growth_weight_Formula':'VARCHAR',
    'Government_expenditure_growth_weight_Logic':'VARCHAR',
    'Government_expenditure_growth_weight_Comments':'VARCHAR',
    'Government_fiscal_deficit%_actual':'FLOAT',
    'Government_fiscal_deficit%_actual_Source':'VARCHAR',
    'Government_fiscal_deficit%_actual_Formula':'VARCHAR',
    'Government_fiscal_deficit%_actual_Logic':'VARCHAR',
    'Government_fiscal_deficit%_actual_Comments':'VARCHAR',
    'Government_fiscal_deficit_weight':'FLOAT',
    'Government_fiscal_deficit_weight_Formula':'VARCHAR',
    'Government_fiscal_deficit_weight_Logic':'VARCHAR',
    'Government_fiscal_deficit_weight_Comments':'VARCHAR',
    'Government_debt_(%GDP)_actual':'FLOAT',
    'Government_debt_(%GDP)_actual_Source':'VARCHAR',
    'Government_debt_(%GDP)_actual_Formula':'VARCHAR',
    'Government_debt_(%GDP)_actual_Logic':'VARCHAR',
    'Government_debt_(%GDP)_actual_Comments':'VARCHAR',
    'Government_debt_(%GDP)_weight':'FLOAT',
    'Government_debt_(%GDP)_weight_Formula':'VARCHAR',
    'Government_debt_(%GDP)_weight_Logic':'VARCHAR',
    'Government_debt_(%GDP)_weight_Comments':'VARCHAR',
    'Labor_force_growth%_actual':'FLOAT',
    'Labor_force_growth%_actual_Source':'VARCHAR',
    'Labor_force_growth%_actual_Formula':'VARCHAR',
    'Labor_force_growth%_actual_Logic':'VARCHAR',
    'Labor_force_growth%_actual_Comments':'VARCHAR',
    'Labor_force_growth_weight':'FLOAT',
    'Labor_force_growth_weight_Formula':'VARCHAR',
    'Labor_force_growth_weight_Logic':'VARCHAR',
    'Labor_force_growth_weight_Comments':'VARCHAR',
    'Private_sector_debt_growth%_actual':'FLOAT',
    'Private_sector_debt_growth%_actual_Source':'VARCHAR',
    'Private_sector_debt_growth%_actual_Formula':'VARCHAR',
    'Private_sector_debt_growth%_actual_Logic':'VARCHAR',
    'Private_sector_debt_growth%_actual_Comments':'VARCHAR',
    'Private_sector_debt_growth_weight':'FLOAT',
    'Private_sector_debt_growth_weight_Formula':'VARCHAR',
    'Private_sector_debt_growth_weight_Logic':'VARCHAR',
    'Private_sector_debt_growth_weight_Comments':'VARCHAR',
    'Exports_growth%_actual':'FLOAT',
    'Exports_growth%_actual_Source':'VARCHAR',
    'Exports_growth%_actual_Formula':'VARCHAR',
    'Exports_growth%_actual_Logic':'VARCHAR',
    'Exports_growth%_actual_Comments':'VARCHAR',
    'Exports_growth_weight':'FLOAT',
    'Exports_growth_weight_Formula':'VARCHAR',
    'Exports_growth_weight_Logic':'VARCHAR',
    'Exports_growth_weight_Comments':'VARCHAR',
    'Imports_growth%_actual':'FLOAT',
    'Imports_growth%_actual_Source':'VARCHAR',
    'Imports_growth%_actual_Formula':'VARCHAR',
    'Imports_growth%_actual_Logic':'VARCHAR',
    'Imports_growth%_actual_Comments':'VARCHAR',
    'Imports_growth_weight':'FLOAT',
    'Imports_growth_weight_Formula':'VARCHAR',
    'Imports_growth_weight_Logic':'VARCHAR',
    'Imports_growth_weight_Comments':'VARCHAR',
    'Currency_stability_actual':'VARCHAR',
    'Currency_stability_actual_Source':'VARCHAR',
    'Currency_stability_actual_Formula':'VARCHAR',
    'Currency_stability_actual_Logic':'VARCHAR',
    'Currency_stability_actual_Comments':'VARCHAR',
    'Currency_stability_weight':'FLOAT',
    'Currency_stability_weight_Formula':'VARCHAR',
    'Currency_stability_weight_Logic':'VARCHAR',
    'Currency_stability_weight_Comments':'VARCHAR',
    'Gross_capital_formation_(GDP%)_actual':'FLOAT',
    'Gross_capital_formation_(GDP%)_actual_Source':'VARCHAR',
    'Gross_capital_formation_(GDP%)_actual_Formula':'VARCHAR',
    'Gross_capital_formation_(GDP%)_actual_Logic':'VARCHAR',
    'Gross_capital_formation_(GDP%)_actual_Comments':'VARCHAR',
    'Gross_capital_formation_(GDP%)_weight':'FLOAT',
    'Gross_capital_formation_(GDP%)_weight_Formula':'VARCHAR',
    'Gross_capital_formation_(GDP%)_weight_Logic':'VARCHAR',
    'Gross_capital_formation_(GDP%)_weight_Comments':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_actual':'FLOAT',
    'foreign_direct_investment_FDI(GDP%)_actual_Source':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_actual_Formula':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_actual_Logic':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_actual_Comments':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_weight':'FLOAT',
    'foreign_direct_investment_FDI(GDP%)_weight_Formula':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_weight_Logic':'VARCHAR',
    'foreign_direct_investment_FDI(GDP%)_weight_Comments':'VARCHAR',
    'Productivity_improvement%_actual':'FLOAT',
    'Productivity_improvement%_actual_Source':'VARCHAR',
    'Productivity_improvement%_actual_Formula':'VARCHAR',
    'Productivity_improvement%_actual_Logic':'VARCHAR',
    'Productivity_improvement%_actual_Comments':'VARCHAR',
    'Productivity_improvement_weight':'FLOAT',
    'Productivity_improvement_weight_Formula':'VARCHAR',
    'Productivity_improvement_weight_Logic':'VARCHAR',
    'Productivity_improvement_weight_Comments':'VARCHAR',
    'TOTAL':'FLOAT',
    'TOTAL_Formula':'VARCHAR',
    'TOTAL_Logic':'VARCHAR',
    'TOTAL_Comments':'VARCHAR',
    'GDP_Revenues':'VARCHAR',
    'Budget_Revenues':'VARCHAR',
    'Budget_Expenses':'VARCHAR',
    'GDP_Revenues_Sources':'VARCHAR',
    'GDP_Revenues_Logic':'VARCHAR',
    'GDP_Revenues_Comments':'VARCHAR',
    'Budget_Revenues_Sources':'VARCHAR',
    'Budget_Revenues_Logic':'VARCHAR',
    'Budget_Revenues_Comments':'VARCHAR',
    'Budget_Expenses_Sources':'VARCHAR',
    'Budget_Expenses_Logic':'VARCHAR',
    'Budget_Expenses_Comments':'VARCHAR',
    'Investment_GDP%_actual':'FLOAT',
    'Investment_GDP%_actual_Source':'VARCHAR',
    'Investment_GDP%_actual_Formula':'VARCHAR',
    'Investment_GDP%_actual_Logic':'VARCHAR',
    'Investment_GDP%_actual_Comments':'VARCHAR',
    'Investment_GDP%_weight':'FLOAT',
    'Investment_GDP%_weight_Formula':'VARCHAR',
    'Investment_GDP%_weight_Logic':'VARCHAR',
    'Investment_GDP%_weight_Comments':'VARCHAR',
    'Investment_growth%_actual':'FLOAT',
    'Investment_growth%_actual_Source':'VARCHAR',
    'Investment_growth%_actual_Formula':'VARCHAR',
    'Investment_growth%_actual_Logic':'VARCHAR',
    'Investment_growth%_actual_Comments':'VARCHAR',
    'Investment_growth_weight':'FLOAT',
    'Investment_growth_weight_Formula':'VARCHAR',
    'Investment_growth_weight_Logic':'VARCHAR',
    'Investment_growth_weight_Comments':'VARCHAR',
    'Innovation(R&D)_economy%_actual':'FLOAT',
    'Innovation(R&D)_economy%_actual_Source':'VARCHAR',
    'Innovation(R&D)_economy%_actual_Formula':'VARCHAR',
    'Innovation(R&D)_economy%_actual_Logic':'VARCHAR',
    'Innovation(R&D)_economy%_actual_Comments':'VARCHAR',
    'Innovation(R&D)_economy_weight':'FLOAT',
    'Innovation(R&D)_economy_weight_Formula':'VARCHAR',
    'Innovation(R&D)_economy_weight_Logic':'VARCHAR',
    'Innovation(R&D)_economy_weight_Comments':'VARCHAR',
    'Interest_rates%_actual':'FLOAT',
    'Interest_rates%_actual_Source':'VARCHAR',
    'Interest_rates%_actual_Formula':'VARCHAR',
    'Interest_rates%_actual_Logic':'VARCHAR',
    'Interest_rates%_actual_Comments':'VARCHAR',
    'Interest_rates_weight':'FLOAT',
    'Interest_rates_weight_Formula':'VARCHAR',
    'Interest_rates_weight_Logic':'VARCHAR',
    'Interest_rates_weight_Comments':'VARCHAR',
    'Exports_growth%_actual':'FLOAT',
    'Exports_growth%_actual_Formula':'VARCHAR',
    'Exports_growth%_actual_Logic':'VARCHAR',
    'Exports_growth%_actual_Comments':'VARCHAR',
    'Exports_growth%_actual_Source':'VARCHAR',
    'Population_growth%_actual':'FLOAT',
    'Population_growth%_actual_Source':'VARCHAR',
    'Population_growth%_actual_Formula':'VARCHAR',
    'Population_growth%_actual_Logic':'VARCHAR',
    'Population_growth%_actual_Comments':'VARCHAR',
    'Population_growth_weight':'FLOAT',
    'Population_growth_weight_Formula':'VARCHAR',
    'Population_growth_weight_Logic':'VARCHAR',
    'Population_growth_weight_Comments':'VARCHAR',
    'Labor_force_growth%_actual':'FLOAT',
    'Labor_force_growth%_actual_Source':'VARCHAR',
    'Labor_force_growth%_actual_Formula':'VARCHAR',
    'Labor_force_growth%_actual_Logic':'VARCHAR',
    'Labor_force_growth%_actual_Comments':'VARCHAR',
    'Labor_force_growth_weight':'FLOAT',
    'Labor_force_growth_weight_Formula':'VARCHAR',
    'Labor_force_growth_weight_Logic':'VARCHAR',
    'Labor_force_growth_weight_Comments':'VARCHAR',
    'Saving_rate%_actual':'FLOAT',
    'Saving_rate%_actual_Source':'VARCHAR',
    'Saving_rate%_actual_Formula':'VARCHAR',
    'Saving_rate%_actual_Logic':'VARCHAR',
    'Saving_rate%_actual_Comments':'VARCHAR',
    'Saving_rate_weight':'FLOAT',
    'Saving_rate_weight_Formula':'VARCHAR',
    'Saving_rate_weight_Logic':'VARCHAR',
    'Saving_rate_weight_Comments':'VARCHAR',
    'Inflation_rate%_actual':'FLOAT',
    'Inflation_rate%_actual_Source':'VARCHAR',
    'Inflation_rate%_actual_Formula':'VARCHAR',
    'Inflation_rate%_actual_Logic':'VARCHAR',
    'Inflation_rate%_actual_Comments':'VARCHAR',
    'Inflation_rate_weight':'FLOAT',
    'Inflation_rate_weight_Formula':'VARCHAR',
    'Inflation_rate_weight_Logic':'VARCHAR',
    'Inflation_rate_weight_Comments':'VARCHAR',
    'Currency_stability_actual':'VARCHAR',
    'Currency_stability_actual_Source':'VARCHAR',
    'Currency_stability_actual_Formula':'VARCHAR',
    'Currency_stability_actual_Logic':'VARCHAR',
    'Currency_stability_actual_Comments':'VARCHAR',
    'Currency_stability_weight':'FLOAT',
    'Currency_stability_weight_Formula':'VARCHAR',
    'Currency_stability_weight_Logic':'VARCHAR',
    'Currency_stability_weight_Comments':'VARCHAR',
    'Central_bank_independence_actual':'VARCHAR',
    'Central_bank_independence_actual_Source':'VARCHAR',
    'Central_bank_independence_actual_Formula':'VARCHAR',
    'Central_bank_independence_actual_Logic':'VARCHAR',
    'Central_bank_independence_actual_Comments':'VARCHAR',
    'Central_bank_independence_weight':'FLOAT',
    'Central_bank_independence_weight_Formula':'VARCHAR',
    'Central_bank_independence_weight_Logic':'VARCHAR',
    'Central_bank_independence_weight_Comments':'VARCHAR',
    'Exports_growth%_actual':'FLOAT',
    'Exports_growth%_actual_Formula':'VARCHAR',
    'Exports_growth%_actual_Logic':'VARCHAR',
    'Exports_growth%_actual_Comments':'VARCHAR',
    'Exports_growth%_actual_Source':'VARCHAR',
    'Exports_growth_weight':'FLOAT',
    'Exports_growth_weight_Formula':'VARCHAR',
    'Exports_growth_weight_Logic':'VARCHAR',
    'Exports_growth_weight_Comments':'VARCHAR',
    'Imports_growth%_actual':'FLOAT',
    'Imports_growth%_actual_Source':'VARCHAR',
    'Imports_growth%_actual_Formula':'VARCHAR',
    'Imports_growth%_actual_Logic':'VARCHAR',
    'Imports_growth%_actual_Comments':'VARCHAR',
    'Imports_growth_weight':'FLOAT',
    'Imports_growth_weight_Formula':'VARCHAR',
    'Imports_growth_weight_Logic':'VARCHAR',
    'Imports_growth_weight_Comments':'VARCHAR',
    'Trade_balance_billion_dollar_actual':'FLOAT',
    'Trade_balance_billion_dollar_actual_Source':'VARCHAR',
    'Trade_balance_billion_dollar_actual_Formula':'VARCHAR',
    'Trade_balance_billion_dollar_actual_Logic':'VARCHAR',
    'Trade_balance_billion_dollar_actual_Comments':'VARCHAR',
    'Trade_balance_weight':'FLOAT',
    'Trade_balance_weight_Formula':'VARCHAR',
    'Trade_balance_weight_Logic':'VARCHAR',
    'Trade_balance_weight_Comments':'VARCHAR',
    'Fiscal_deficit_million_dollar_actual':'FLOAT',
    'Fiscal_deficit_million_dollar_actual_Source':'VARCHAR',
    'Fiscal_deficit_million_dollar_actual_Formula':'VARCHAR',
    'Fiscal_deficit_million_dollar_actual_Logic':'VARCHAR',
    'Fiscal_deficit_million_dollar_actual_Comments':'VARCHAR',
    'Fiscal_deficit_weight':'FLOAT',
    'Fiscal_deficit_weight_Formula':'VARCHAR',
    'Fiscal_deficit_weight_Logic':'VARCHAR',
    'Fiscal_deficit_weight_Comments':'VARCHAR',
    'External_debt_(GPD%)_actual':'FLOAT',
    'External_debt_(GPD%)_actual_Formula':'VARCHAR',
    'External_debt_(GPD%)_actual_Logic':'VARCHAR',
    'External_debt_(GPD%)_actual_Comments':'VARCHAR',
    'External_debt_(GPD%)_actual_Source':'VARCHAR',
    'External_debt_(GPD%)_weight':'FLOAT',
    'External_debt_(GPD%)_weight_Formula':'VARCHAR',
    'External_debt_(GPD%)_weight_Logic':'VARCHAR',
    'External_debt_(GPD%)_weight_Comments':'VARCHAR',
    'sector':'VARCHAR',
    'subsector':'VARCHAR',
    'title':'VARCHAR',
    'description':'VARCHAR',
    'approximate_cost':'VARCHAR',
    'return_on_investment':'VARCHAR',
    'macroeconomic_stability_actual%':'FLOAT',
    'macroeconomic_stability_actual_Source':'VARCHAR',
    'macroeconomic_stability_actual%_Formula':'VARCHAR',
    'macroeconomic_stability_actual%_Logic':'VARCHAR',
    'macroeconomic_stability_actual%_Comments':'VARCHAR',
    'macroeconomic_stability_weight':'FLOAT',
    'macroeconomic_stability_weight_Formula':'VARCHAR',
    'macroeconomic_stability_weight_Logic':'VARCHAR',
    'macroeconomic_stability_weight_Comments':'VARCHAR',
    'policy_uncertainty_actual%':'FLOAT',
    'policy_uncertainty_actual_Source':'VARCHAR',
    'policy_uncertainty_actual%_Formula':'VARCHAR',
    'policy_uncertainty_actual%_Logic':'VARCHAR',
    'policy_uncertainty_actual%_Comments':'VARCHAR',
    'policy_uncertainty_weight':'FLOAT',
    'policy_uncertainty_weight_Formula':'VARCHAR',
    'policy_uncertainty_weight_Logic':'VARCHAR',
    'policy_uncertainty_weight_Comments':'VARCHAR',
    'corruption_actual%':'FLOAT',
    'corruption_actual_Source':'VARCHAR',
    'corruption_actual%_Formula':'VARCHAR',
    'corruption_actual%_Logic':'VARCHAR',
    'corruption_actual%_Comments':'VARCHAR',
    'corruption_weight':'FLOAT',
    'corruption_weight_Formula':'VARCHAR',
    'corruption_weight_Logic':'VARCHAR',
    'corruption_weight_Comments':'VARCHAR',
    'tax_rates_burden_actual%':'FLOAT',
    'tax_rates_burden_actual_Source':'VARCHAR',
    'tax_rates_burden_actual%_Formula':'VARCHAR',
    'tax_rates_burden_actual%_Logic':'VARCHAR',
    'tax_rates_burden_actual%_Comments':'VARCHAR',
    'tax_rates_burden_weight':'FLOAT',
    'tax_rates_burden_weight_Formula':'VARCHAR',
    'tax_rates_burden_weight_Logic':'VARCHAR',
    'tax_rates_burden_weight_Comments':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_actual%':'FLOAT',
    'cost_access_to_finance_GlobalFinanceIndex_actual_Source':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Formula':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Logic':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_actual%_Comments':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_weight':'FLOAT',
    'cost_access_to_finance_GlobalFinanceIndex_weight_Formula':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_weight_Logic':'VARCHAR',
    'cost_access_to_finance_GlobalFinanceIndex_weight_Comments':'VARCHAR',
    'crime_actual%':'FLOAT',
    'crime_actual_Source':'VARCHAR',
    'crime_actual%_Formula':'VARCHAR',
    'crime_actual%_Logic':'VARCHAR',
    'crime_actual%_Comments':'VARCHAR',
    'crime_weight':'FLOAT',
    'crime_weight_Formula':'VARCHAR',
    'crime_weight_Logic':'VARCHAR',
    'crime_weight_Comments':'VARCHAR',
    'regulation_and_tax_administration_actual%':'FLOAT',
    'regulation_and_tax_administration_actual_Source':'VARCHAR',
    'regulation_and_tax_administration_actual%_Formula':'VARCHAR',
    'regulation_and_tax_administration_actual%_Logic':'VARCHAR',
    'regulation_and_tax_administration_actual%_Comments':'VARCHAR',
    'regulation_and_tax_administration_weight':'FLOAT',
    'regulation_and_tax_administration_weight_Formula':'VARCHAR',
    'regulation_and_tax_administration_weight_Logic':'VARCHAR',
    'regulation_and_tax_administration_weight_Comments':'VARCHAR',
    'skills-based_economy_SBEI_actual%':'FLOAT',
    'skills-based_economy_SBEI_actual_Source':'VARCHAR',
    'skills-based_economy_SBEI_actual%_Formula':'VARCHAR',
    'skills-based_economy_SBEI_actual%_Logic':'VARCHAR',
    'skills-based_economy_SBEI_actual%_Comments':'VARCHAR',
    'skills-based_economy_SBEI_weight':'FLOAT',
    'skills-based_economy_SBEI_weight_Formula':'VARCHAR',
    'skills-based_economy_SBEI_weight_Logic':'VARCHAR',
    'skills-based_economy_SBEI_weight_Comments':'VARCHAR',
    'quality_of_education_primary_tertiary_actual%':'FLOAT',
    'quality_of_education_primary_tertiary_actual_Source':'VARCHAR',
    'quality_of_education_primary_tertiary_actual%_Formula':'VARCHAR',
    'quality_of_education_primary_tertiary_actual%_Logic':'VARCHAR',
    'quality_of_education_primary_tertiary_actual%_Comments':'VARCHAR',
    'quality_of_education_primary_tertiary_weight':'FLOAT',
    'quality_of_education_primary_tertiary_weight_Formula':'VARCHAR',
    'quality_of_education_primary_tertiary_weight_Logic':'VARCHAR',
    'quality_of_education_primary_tertiary_weight_Comments':'VARCHAR',
    'quality_of_healthcare_actual%':'FLOAT',
    'quality_of_healthcare_actual_Source':'VARCHAR',
    'quality_of_healthcare_actual%_Formula':'VARCHAR',
    'quality_of_healthcare_actual%_Logic':'VARCHAR',
    'quality_of_healthcare_actual%_Comments':'VARCHAR',
    'quality_of_healthcare_weight':'FLOAT',
    'quality_of_healthcare_weight_Formula':'VARCHAR',
    'quality_of_healthcare_weight_Logic':'VARCHAR',
    'quality_of_healthcare_weight_Comments':'VARCHAR',
    'rule_of_law_actual%':'FLOAT',
    'rule_of_law_actual_Source':'VARCHAR',
    'rule_of_law_actual%_Formula':'VARCHAR',
    'rule_of_law_actual%_Logic':'VARCHAR',
    'rule_of_law_actual%_Comments':'VARCHAR',
    'rule_of_law_weight':'FLOAT',
    'rule_of_law_weight_Formula':'VARCHAR',
    'rule_of_law_weight_Logic':'VARCHAR',
    'rule_of_law_weight_Comments':'VARCHAR',
    'transportation_actual%':'FLOAT',
    'transportation_actual_Source':'VARCHAR',
    'transportation_actual%_Formula':'VARCHAR',
    'transportation_actual%_Logic':'VARCHAR',
    'transportation_actual%_Comments':'VARCHAR',
    'transportation_weight':'FLOAT',
    'transportation_weight_Formula':'VARCHAR',
    'transportation_weight_Logic':'VARCHAR',
    'transportation_weight_Comments':'VARCHAR',
    'telecommunication_actual%':'FLOAT',
    'telecommunication_actual_Source':'VARCHAR',
    'telecommunication_actual%_Formula':'VARCHAR',
    'telecommunication_actual%_Logic':'VARCHAR',
    'telecommunication_actual%_Comments':'VARCHAR',
    'telecommunication_weight':'FLOAT',
    'telecommunication_weight_Formula':'VARCHAR',
    'telecommunication_weight_Logic':'VARCHAR',
    'telecommunication_weight_Comments':'VARCHAR',
    'digitalization_actual%':'FLOAT',
    'digitalization_actual_Source':'VARCHAR',
    'digitalization_actual%_Formula':'VARCHAR',
    'digitalization_actual%_Logic':'VARCHAR',
    'digitalization_actual%_Comments':'VARCHAR',
    'digitalization_weight':'FLOAT',
    'digitalization_weight_Formula':'VARCHAR',
    'digitalization_weight_Logic':'VARCHAR',
    'digitalization_weight_Comments':'VARCHAR',
    'cost_of_living_actual%':'FLOAT',
    'cost_of_living_actual_Source':'VARCHAR',
    'cost_of_living_actual%_Formula':'VARCHAR',
    'cost_of_living_actual%_Logic':'VARCHAR',
    'cost_of_living_actual%_Comments':'VARCHAR',
    'cost_of_living_weight':'FLOAT',
    'cost_of_living_weight_Formula':'VARCHAR',
    'cost_of_living_weight_Logic':'VARCHAR',
    'cost_of_living_weight_Comments':'VARCHAR',
    'quality_of_living_actual%':'FLOAT',
    'quality_of_living_actual_Source':'VARCHAR',
    'quality_of_living_actual%_Formula':'VARCHAR',
    'quality_of_living_actual%_Logic':'VARCHAR',
    'quality_of_living_actual%_Comments':'VARCHAR',
    'quality_of_living_weight':'FLOAT',
    'quality_of_living_weight_Formula':'VARCHAR',
    'quality_of_living_weight_Logic':'VARCHAR',
    'quality_of_living_weight_Comments':'VARCHAR',
    'GPI_Global_Peace_Actual':'FLOAT',
    'GPI_Global_Peace_Actual_Source':'VARCHAR',
    'GPI_Global_Peace_Actual_Formula':'VARCHAR',
    'GPI_Global_Peace_Actual_Logic':'VARCHAR',
    'GPI_Global_Peace_Actual_Comments':'VARCHAR',
    'GPI_Global_Peace_Weight':'FLOAT',
    'GPI_Global_Peace_Weight_Formula':'VARCHAR',
    'GPI_Global_Peace_Weight_Logic':'VARCHAR',
    'GPI_Global_Peace_Weight_Comments':'VARCHAR',
    'PSI_Political_Stability_Actual':'FLOAT',
    'PSI_Political_Stability_Actual_Source':'VARCHAR',
    'PSI_Political_Stability_Actual_Formula':'VARCHAR',
    'PSI_Political_Stability_Actual_Logic':'VARCHAR',
    'PSI_Political_Stability_Actual_Comments':'VARCHAR',
    'PSI_Political_Stability_Weight':'FLOAT',
    'PSI_Political_Stability_Weight_Formula':'VARCHAR',
    'PSI_Political_Stability_Weight_Logic':'VARCHAR',
    'PSI_Political_Stability_Weight_Comments':'VARCHAR',
    'CPI_Corruption_Perception_Actual':'FLOAT',
    'CPI_Corruption_Perception_Actual_Source':'VARCHAR',
    'CPI_Corruption_Perception_Actual_Formula':'VARCHAR',
    'CPI_Corruption_Perception_Actual_Logic':'VARCHAR',
    'CPI_Corruption_Perception_Actual_Comments':'VARCHAR',
    'CPI_Corruption_Perception_Weight':'FLOAT',
    'CPI_Corruption_Perception_Weight_Formula':'VARCHAR',
    'CPI_Corruption_Perception_Weight_Logic':'VARCHAR',
    'CPI_Corruption_Perception_Weight_Comments':'VARCHAR',
    'GTI_Global_Terrorism_Actual':'FLOAT',
    'GTI_Global_Terrorism_Actual_Source':'VARCHAR',
    'GTI_Global_Terrorism_Actual_Formula':'VARCHAR',
    'GTI_Global_Terrorism_Actual_Logic':'VARCHAR',
    'GTI_Global_Terrorism_Actual_Comments':'VARCHAR',
    'GTI_Global_Terrorism_Weight':'FLOAT',
    'GTI_Global_Terrorism_Weight_Formula':'VARCHAR',
    'GTI_Global_Terrorism_Weight_Logic':'VARCHAR',
    'GTI_Global_Terrorism_Weight_Comments':'VARCHAR',
    'WRI_World_Risk_Actual':'FLOAT',
    'WRI_World_Risk_Actual_Source':'VARCHAR',
    'WRI_World_Risk_Actual_Formula':'VARCHAR',
    'WRI_World_Risk_Actual_Logic':'VARCHAR',
    'WRI_World_Risk_Actual_Comments':'VARCHAR',
    'WRI_World_Risk_Weight':'FLOAT',
    'WRI_World_Risk_Weight_Formula':'VARCHAR',
    'WRI_World_Risk_Weight_Logic':'VARCHAR',
    'WRI_World_Risk_Weight_Comments':'VARCHAR',
    'HDI_Human_Development_Actual':'FLOAT',
    'HDI_Human_Development_Actual_Source':'VARCHAR',
    'HDI_Human_Development_Actual_Formula':'VARCHAR',
    'HDI_Human_Development_Actual_Logic':'VARCHAR',
    'HDI_Human_Development_Actual_Comments':'VARCHAR',
    'HDI_Human_Development_Weight':'FLOAT',
    'HDI_Human_Development_Weight_Formula':'VARCHAR',
    'HDI_Human_Development_Weight_Logic':'VARCHAR',
    'HDI_Human_Development_Weight_Comments':'VARCHAR',
    'TI_Transparency_Actual':'FLOAT',
    'TI_Transparency_Actual_Source':'VARCHAR',
    'TI_Transparency_Actual_Formula':'VARCHAR',
    'TI_Transparency_Actual_Logic':'VARCHAR',
    'TI_Transparency_Actual_Comments':'VARCHAR',
    'TI_Transparency_Weight':'FLOAT',
    'TI_Transparency_Weight_Formula':'VARCHAR',
    'TI_Transparency_Weight_Logic':'VARCHAR',
    'TI_Transparency_Weight_Comments':'VARCHAR',
    'BEI_Business_Enviroment_Actual':'FLOAT',
    'BEI_Business_Enviroment_Actual_Source':'VARCHAR',
    'BEI_Business_Enviroment_Actual_Formula':'VARCHAR',
    'BEI_Business_Enviroment_Actual_Logic':'VARCHAR',
    'BEI_Business_Enviroment_Actual_Comments':'VARCHAR',
    'BEI_Business_Enviroment_Weight':'FLOAT',
    'BEI_Business_Enviroment_Weight_Formula':'VARCHAR',
    'BEI_Business_Enviroment_Weight_Logic':'VARCHAR',
    'BEI_Business_Enviroment_Weight_Comments':'VARCHAR',
    'WJP_Rule_of_Law_Actual':'FLOAT',
    'WJP_Rule_of_Law_Actual_Source':'VARCHAR',
    'WJP_Rule_of_Law_Actual_Formula':'VARCHAR',
    'WJP_Rule_of_Law_Actual_Logic':'VARCHAR',
    'WJP_Rule_of_Law_Actual_Comments':'VARCHAR',
    'WJP_Rule_of_Law_Weight':'FLOAT',
    'WJP_Rule_of_Law_Weight_Formula':'VARCHAR',
    'WJP_Rule_of_Law_Weight_Logic':'VARCHAR',
    'WJP_Rule_of_Law_Weight_Comments':'VARCHAR',
    'VAI_Voice_and_Accountability_Actual':'FLOAT',
    'VAI_Voice_and_Accountability_Actual_Source':'VARCHAR',
    'VAI_Voice_and_Accountability_Actual_Formula':'VARCHAR',
    'VAI_Voice_and_Accountability_Actual_Logic':'VARCHAR',
    'VAI_Voice_and_Accountability_Actual_Comments':'VARCHAR',
    'VAI_Voice_and_Accountability_Weight':'FLOAT',
    'VAI_Voice_and_Accountability_Weight_Formula':'VARCHAR',
    'VAI_Voice_and_Accountability_Weight_Logic':'VARCHAR',
    'VAI_Voice_and_Accountability_Weight_Comments':'VARCHAR',
    'OCI_Organized_Crime_Actual':'FLOAT',
    'OCI_Organized_Crime_Actual_Source':'VARCHAR',
    'OCI_Organized_Crime_Actual_Formula':'VARCHAR',
    'OCI_Organized_Crime_Actual_Logic':'VARCHAR',
    'OCI_Organized_Crime_Actual_Comments':'VARCHAR',
    'OCI_Organized_Crime_Weight':'FLOAT',
    'OCI_Organized_Crime_Weight_Formula':'VARCHAR',
    'OCI_Organized_Crime_Weight_Logic':'VARCHAR',
    'OCI_Organized_Crime_Weight_Comments':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Actual':'FLOAT',
    'FHPRI_Freedom_House_Political_Rights_Actual_Source':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Actual_Formula':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Actual_Logic':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Actual_Comments':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Weight':'FLOAT',
    'FHPRI_Freedom_House_Political_Rights_Weight_Formula':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Weight_Logic':'VARCHAR',
    'FHPRI_Freedom_House_Political_Rights_Weight_Comments':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Actual':'FLOAT',
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Source':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Formula':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Logic':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Actual_Comments':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Weight':'FLOAT',
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Formula':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Logic':'VARCHAR',
    'FHCFI_Freedom_House_Civil_Liberties_Weight_Comments':'VARCHAR',
    'DI_Democracy_Actual':'FLOAT',
    'DI_Democracy_Actual_Source':'VARCHAR',
    'DI_Democracy_Actual_Formula':'VARCHAR',
    'DI_Democracy_Actual_Logic':'VARCHAR',
    'DI_Democracy_Actual_Comments':'VARCHAR',
    'DI_Democracy_Weight':'FLOAT',
    'DI_Democracy_Weight_Formula':'VARCHAR',
    'DI_Democracy_Weight_Logic':'VARCHAR',
    'DI_Democracy_Weight_Comments':'VARCHAR',
    'result':'VARCHAR', 
    'recommendation':'VARCHAR', 
    'video':'VARCHAR',
    'main_sector':'VARCHAR',
    'subsector':'VARCHAR', 
    'available':'INT'}
    

    # Convert the DataFrame columns to the expected data types
    for column_en, expected_type_en in expected_data_types_en.items():
        if column_en in data_en.columns:
            if expected_type_en == 'VARCHAR':
                try:
                    data_en[column_en].iloc[-1] = int(data_en[column_en].iloc[-1])
                except:
                    pass
                if type(data_en[column_en].iloc[-1]) == int:
                    err = f"الرجاء ادخاء المعلومات بصيغة كلمات في {column_en}"
                    st.error(err)
                    raise 'Stop'
                else:
                    data_en[column_en].iloc[-1] = str(data_en[column_en].iloc[-1])
                    if len(data_en[column_en].iloc[-1]) > 10000:
                        err = f"المعلومات التي ادخلتها طويلة في {column_en}"
                        st.error(err)
                        raise 'Stop'
            elif expected_type_en == 'INT':
                try:
                    data_en[column_en].iloc[-1] = int(data_en[column_en].iloc[-1])
                except Exception as e:
                    err = f"الرجاء ادخاء المعلومات بصيغة ارقام صحيحة في {column_en}"
                    st.error(err)
                    raise 'Stop'
            elif expected_type_en == 'FLOAT':
                try:
                    data_en[column_en].iloc[-1] = float(data_en[column_en].iloc[-1])
                except Exception as e:
                    err = f"الرجاء ادخاء المعلومات بصيغة ارقام عشرية في {column_en}"
                    st.error(err)
                    raise 'Stop'

    return data_en, table_name_en, expected_dtypes_en

def convert_to_million(value, unit):
    conversions = {
        'مليون': 1,
        'مليار': 1000,
        'تريليون': 1000000,
        # Add more units as needed
    }
    o = float(value) * conversions[unit]

    return o


def convert_to_billion(value, unit):
    conversions = {
        'مليون': 0.001,
        'مليار': 1,
        'تريليون': 1000,
        # Add more units as needed
    }
    o = float(value) * conversions[unit]

    return o


# Streamlit app
st.title("Country Data Editor")

# Define the main page and buttons
page = st.radio("Select Page", ["Add Country", "Update Country"])

columns_to_convert_to_million = ['إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار',
                                 'قيمة_الصادرات_بالمليون_دولار',
                                 'عجز_ميزان_المدفوعات_بالمليون_دولار',
                                 ]

columns_to_convert_to_billion = ['الناتج_المحلي_الاجمالي_بالمليار_دولار',
                                 'الناتج_القومي_الاجمالي_بالمليار_دولار',
                                 'حجم_الموازنة_العامة_للنفقات_بالمليار',
                                 'العجز_الكلي_في_الموازنة_العامة_للدولة_بعد_المنح_بالمليار',
                                 'الاستثمار_الأجنبي_المباشر_بالمليار_دولار',
                                 'احتياطات_النقد_الأجنبي_بالمليار_دولار',
                                 'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار',
                                 'حجم_الموازنة_العامة_للنفقات_بالمليار',
                                 'الميزان_التجاري_بالمليار_دولار',
                                 'الميزان_التجاري_مليار_Actual',
                                 'قيمة_الواردات_بالمليار_دولار',
                                 'الناتج_المحلي_الإجمالي_مليار$_Actual'
                                 ]

precentage_col = ['الدولة',
                  'اللغة_الرسمية',
                  'العاصمة',
                  'العملة',
                  'اللغة الرسمية',
                  'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)',
                  'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)',
                  'أبرز_الصادرات',
                  'أبرز_الواردات',
                  'استقلالية_البنك_المركزي_Actual',
                  'الاستقرار_النقدي_Actual',
                  'إيرادات_الموازنة_العامة',
                  'التوصية',
                  'النتيجة',
                  'إيرادات_الناتج_المحلي_الإجمالي',
                  'نفقات_الموازنة_العامة',
                  'فيديو',
                  'عدد_السكان_Comments',
                  'نسبة_النمو_السكاني%_Comments',
                  'متوسط_عمر_السكان_ذكر_Comments',
                  'متوسط_عمر_السكان_أنثى_Comments',
                  'نسبة_البطالة%_Comments',
                  'الحد_الأدنى_للأجور_شهري_بالدولار_Comments',
                  'نسبة_السكان_تحت_خط_الفقر_المحلي%_Comments',
                  'متوسط_الدخل_للاسرة_سنوي_بالدولار_Comments',
                  'الناتج_المحلي_الاجمالي_بالمليار_دولار_Comments',
                  'الناتج_المحلي_الإجمالي_للفرد_سنوي_بالدولار_Comments',
                  'متوسط_الدخل_الفردي_سنوي_بالدولار_Comments',
                  'سعر_صرف_العملة_مقابل_الدولار_Comments',
                  'نسبة_النمو_بالناتج_المحلي%_Comments',
                  'الناتج_القومي_الاجمالي_بالمليار_دولار_Comments',
                  'حجم_الموازنة_العامة_للنفقات_بالمليار_Comments',
                  'GDP%_نسبة_الموازنة_العامة_Comments',
                  'سنة_الموازنة_العامة_Comments',
                  'إجمالي_إيرادات_الموازنة_العامة_بالمليون_دولار_Comments',
                  'العجز_الكلي_الموازنة_العامة_للدولة_بعد_المنح_بالمليار_Comments',
                  'الدين_العام_إلى_الناتج_المحلي_الإجمالي%_Comments',
                  'نسبة_التضخم%_Comments',
                  'العجز_الكلي_إلى_الناتج_المحلي_الإجمالي_بعد_المنح%_Comments',
                  'الديون_الخارجية_إلى_الناتج_المحلي_الإجمالي%_Comments',
                  'الميزان_التجاري_بالمليار_دولار_Comments',
                  'قيمة_الواردات_بالمليار_دولار_Comments',
                  'قيمة_الصادرات_بالمليون_دولار_Comments',
                  'عجز_ميزان_المدفوعات_بالمليون_دولار_Comments',
                  'ميزان_المدفوعات_إلى_الناتج_المحلي_الإجمالي%_Comments',
                  'الاستثمار_الأجنبي_المباشر_بالمليار_دولار_Comments',
                  'فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)_Comments',
                  'فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)_Comments',
                  'احتياطات_النقد_الأجنبي_بالمليار_دولار_Comments',
                  'نسبة_الفائدة_على_الودائع%_Comments',
                  'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/كمبيالات%_Comments',
                  'نسبة_الفائدة_التسهيلات_الإئتمانية_للبنوك/جاري-مدين%_Comments',
                  'الميزانية_العمومية_للبنك_المركزي_بالمليار_دولار_Comments',
                  'نسبة_ضريبة_المبيعات%_Comments',
                  'نسبة_ضريبة_الدخل_على_الفرد%_Comments',
                  'نسبة_ضريبة_الدخل_على_الشركات%_Comments',
                  'ضريبة_الأرباح%_Comments',
                  'ضريبة_الارباح_قطاع_البنوك%_Comments',
                  'مؤشر_الفساد_Comments',
                  'الترتيب_العالمي_على_مؤشر_الفساد_Comments',
                  'مؤشر_سهولة_ممارسة_أنشطة_الأعمال_Comments',
                  'كثافة_مؤسسات_الأعمال_الجديدة_Comments',
                  'S&P_التصنيف_الائتماني_حسب_مؤشر_Comments',
                  "Moody's_التصنيف_الائتماني_حسب_مؤشر_Comments",
                  'Fitch_التصنيف_الائتماني_حسب_مؤشر_Comments',
                  'أبرز_الصادرات_Comments',
                  'أبرز_الواردات_Comments',
                  'الناتج_المحلي_الإجمالي_مليون$_Actual_Comments',
                  'الناتج_المحلي_الإجمالي_مليون$_Weight_Comments',
                  '%النمو_في_الناتج_المحلي_الإجمالي_Actual_Comments',
                  'النمو_في_الناتج_المحلي_الإجمالي_Weight_Comments',
                  'النمو_في_الإنفاق_الاستهلاكي%_Actual_Comments',
                  'النمو_في_الإنفاق_الاستهلاكي_Weight_Comments',
                  'نمو_الاستثمار%_Actual_Comments',
                  'نمو_الاستثمار_Weight_Comments',
                  'النمو_في_الإنفاق_الحكومي%_Actual_Comments',
                  'النمو_في_الإنفاق_الحكومي_Weight_Comments',
                  'العجز_المالي_الحكومي%_Actual_Comments',
                  'العجز_المالي_الحكومي_Weight_Comments',
                  'GDP%_الدين_الحكومي_Actual_Comments',
                  'الدين_الحكومي_Weight_Comments',
                  'النمو_في_القوة_العمالية_Actual_Comments',
                  'النمو_في_القوة_العمالية_Weight_Comments',
                  'دين_القطاع_الخاص_Weight_Comments',
                  'دين_القطاع_الخاص%_Actual_Comments',
                  'نمو_الصادرات%_Actual_Comments',
                  'نمو_الصادرات_Weight_Comments',
                  'نمو_الواردات%_Actual_Comments',
                  'نمو_الواردات_Weight_Comments',
                  'الاستقرار_النقدي_Actual_Comments',
                  'الاستقرار_النقدي_Weight_Comments',
                  'إجمالي_تكوين_رأس_المال%_Actual_Comments',
                  'إجمالي_تكوين_رأس_المال_Weight_Comments',
                  'GDP%_صافي_الاستثمار_الأجنبي_Actual_Comments',
                  'صافي_الاستثمار_الأجنبي_Weight_Comments',
                  'تعزيز_الانتاجية%_Actual_Comments',
                  'تعزيز_الانتاجية_Weight_Comments',
                  'المجموع_Comments',
                  'إيرادات_الناتج_المحلي_الإجمالي_Comments',
                  'إيرادات_الموازنة_العامة_Comments',
                  'نفقات_الموازنة_العامة_Comments',
                  '(GDP%)_الاستثمار_Actual_Comments',
                  '(GDP%)_الاستثمار_Weight_Comments',
                  'نمو_الاستثمار_Actual_Comments',
                  '%الابتكار_في_الاقتصاد_Actual_Comments',
                  'الابتكار_في_الاقتصاد_Weight_Comments',
                  '%الفائدة_على_الإقراض_Actual_Comments',
                  'الفائدة_على_الإقراض_Weight_Comments',
                  'النمو_السكاني%_Actual_Comments',
                  'النمو_السكاني_Weight_Comments',
                  'نمو_القوة_العمالية%_Actual_Comments',
                  'نمو_القوة_العمالية_Weight_Comments',
                  'الفائدة_على_الودائع%_Actual_Comments',
                  'الفائدة_على_الودائع_Weight_Comments',
                  'التضخم_Actual_Comments',
                  'التضخم_Weight_Comments',
                  'الاستقرار_النقدي_Actual_Comments',
                  'الاستقرار_النقدي_Weight_Comments',
                  'استقلالية_البنك_المركزي_Actual_Comments',
                  'استقلالية_البنك_المركزي_Weight_Comments',
                  'نمو_الصادرات%_Actual_Comments',
                  'نمو_الصادرات%_Weight_Comments',
                  'نمو_الواردات%_Actual_Comments',
                  'الميزان_التجاري_مليار$_Actual_Comments',
                  'الميزان_التجاري_مليار$_Weight_Comments',
                  'نمو_الواردات%_Weight_Comments',
                  'العجز_النقدي%_Actual_Comments',
                  'العجز_النقدي_Weight_Comments',
                  '(GDP%)_الدين_الخارجي_Actual_Comments',
                  'الدين_الخارجي_Weight_Comments',
                  '%استقرار_الاقتصاد_الكلي_Actual_Comments',
                  'استقرار_الاقتصاد_الكلي_Weight_Comments',
                  'عدم_اليقين_في_السياسات%_Actual_Comments',
                  'عدم_اليقين_في_السياسات_Weight_Comments',
                  'الفساد%_Actual_Comments',
                  'الفساد_Weight_Comments',
                  'معدل_الضرائب%_Actual_Comments',
                  'معدل_الضرائب_Weight_Comments',
                  'التكلفة_والحصول_على_التمويل%_Actual_Comments',
                  'التكلفة_والحصول_على_التمويل_Weight_Comments',
                  'الجريمة%_Actual_Comments',
                  'الجريمة_Weight_Comments',
                  'اللوائح_وإدارة_الضرائب%_Actual_Comments',
                  'اللوائح_وإدارة_الضرائب_Weight_Comments',
                  'المهارات_الأساسية_في_الاقتصاد_Actual_Comments',
                  'المهارات_الأساسية_في_الاقتصاد_Weight_Comments',
                  'جودة_التعليم_الابتدائي_والعالي%_Actual_Comments',
                  'جودة_التعليم_الابتدائي_والعالي_Weight_Comments',
                  'جودة_العناية_الصحية%_Actual_Comments',
                  'جودة_العناية_الصحية_Weight_Comments',
                  '%نظام_المحاكم_Actual_Comments',
                  'نظام_المحاكم_Weight_Comments',
                  'النقل%_Actual_Comments',
                  'النقل_Weight_Comments',
                  'الاتصالات%_Actual_Comments',
                  'الاتصالات_Weight_Comments',
                  'الرقمنة_Actual_Comments',
                  'الرقمنة_Weight_Comments',
                  'تكاليف_المعيشة%_Actual_Comments',
                  'تكاليف_المعيشة_Weight_Comments',
                  'جودة_المعيشة%_Actual_Comments',
                  'جودة_المعيشة_Weight_Comments',
                  'GPI_السلام_العالمي_Actual_Comments',
                  'GPI_السلام_العالمي_Weight_Comments',
                  'PSI_الاستقرار_السياسي_العالمي_Actual_Comments',
                  'PSI_الاستقرار_السياسي_العالمي_Weight_Comments',
                  'CPI_مدركات_الفساد_Actual_Comments',
                  'CPI_مدركات_الفساد_Weight_Comments',
                  'GTI_مكافحة_الإرهاب_Actual_Comments',
                  'GTI_مكافحة_الإرهاب_Weight_Comments',
                  'WRI_مخاطر_الكوارث_الطبيعية_Actual_Comments',
                  'WRI_مخاطر_الكوارث_الطبيعية_Weight_Comments',
                  'HDI_التنمية_البشرية_Actual_Comments',
                  'HDI_التنمية_البشرية_Weight_Comments',
                  'TI_الشفافية_العالمي_Actual_Comments',
                  'TI_الشفافية_العالمي_Weight_Comments',
                  'BEI_بيئة_الأعمال_Actual_Comments',
                  'BEI_بيئة_الأعمال_Weight_Comments',
                  'WJP_سيادة_القانون_Actual_Comments',
                  'WJP_سيادة_القانون_Weight_Comments',
                  'VAI_المشاركة_والمساءلة_Actual_Comments',
                  'VAI_المشاركة_والمساءلة_Weight_Comments',
                  'OCI_الجريمة_المنظمة_Actual_Comments',
                  'OCI_الجريمة_المنظمة_Weight_Comments',
                  'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Actual_Comments',
                  'FHPRI_فريدوم_هاوس_للحقوق_السياسسة_Weight_Comments',
                  'FHCFI_فريدوم_هاوس_للحريات_المدنية_Actual_Comments',
                  'FHCFI_فريدوم_هاوس_للحريات_المدنية_Weight_Comments',
                  'DI_الديمقراطية_Actual_Comments',
                  'DI_الديمقراطية_Weight_Comments',
                  'القطاع_الرئيسي',
                  'القطاع_الفرعي',
                  'القطاع',
                  'العنوان',
                  'الوصف',
                  'التكلفة_التقريبية',
                  'العائد_على_الاستثمار']


main_sectors_en = ['Agriculture','Communication Services','Consumer Staples','Eduction'
,'Energy','Financials','Healthcare','Industrials','Information Technology'
,'Materials','Mining','Real Estate','Tourism','Transportation & Logistics'
,'Utilities']
main_sectors = ['الزراعة','خدمات الاتصالات','السلع الاستهلاكية','التعليم'
,"الطاقة","المالية","الرعاية الصحية","الصناعات","تكنولوجيا المعلومات"
,"المواد","التعدين","العقارات","السياحة","النقل والخدمات اللوجستية"
,'خدمات']
sub_sectors_en = ['Agricultural Production and Distribution',
 'Agriculture Machinery and Equipment','Agriculture services',
 'Agriculture Technology','Animal husbandry','Crop production',
 'Fertilizer','Fishing (commercial fishing, aquaculture)',
 'Forestry (timber production, pulp and paper production)',
 'Integrated Farms','Irrigation and Water Management',
 'Organic Agriculture','Seed and Genetics Production and Development',
 'Sustainable Agriculture ','Tuber Production','Advertising',
 'Data and Internet Service',
 'Entertainment (movie theaters, amusement parks, sports teams)',
 'Interactive Media and Services','Internet Content Information',
 'Market Research','Media','Printing Services','Public Relations',
 'Publishing','Telecommunication Services','Baby and Infant Products',
 'Department Stores','Food and Staples Retailing','Grocery Stores',
 'Household Products','Personal Care Products','Speciality Foods',
 'Specialty Stores','Tobacco Products',
 'Corporate Training and Development',
 'Early Childhood Education and Care (ECEC)','Educational centers',
 'Educational products/publishing',
 'Educational support services (i.e. testing services, consulting, etc.)',
 'Higher Education','Language and Test Prep Schools','Primary schools',
 'Secondary schools','Smart Education and Learning',
 'Student Housing and Services','Vocational and Technical Education ',
 'Alternative Fuels','Biomass Energy','Coal Energy',
 'Electricity Transmission/Transportation and storage ',
 'Geothermal Energy','Hydropower','Lithium Battery Production',
 'Oil and gas drilling','Oil and gas equipment and services',
 'Oil and gas refining and marketing and production ',
 'Oil and gas storage and transportation','Solar Energy','Wind Energy',
 'Banks','Bonds','Cryptocurrencies','Financial Technology','Insurance',
 'Investment Services / Asset Management',
 'Real Estate Investment Trusts (REITs)','Risk Management','Stock Market',
 'Biotechnology','Clinics','Healthcare Distribution',
 'Healthcare equipment and supplies','Hospitals','Long Term Managed Care',
 'Medical Laboratories','Mental Healthcare','Pharmaceuticals',
 'Rehabilitation and Physical Therapy','Veterinary Services',
 'Aerospace and Defense','Aircraft Manufacturing',
 'Automobile manufacturing','Cable and Satellite Equipment',
 'Construction and Engineering (building and maintenance of infrastructure such as roads, bridges, and buildings)',
 'Electrical equipment Manufacturing','Electronics Manufacturing',
 'Environmental Industry','Fabricated Metals',
 'Food and Beverage production',
 'Machinery (industrial, agriculture, and construction)',
 'Nanotechnology Industries','Railroads','Shipbuilding Industry',
 'Silica Manufacturing',
 'Textiles and apparel manufacturing (fabrics, clothing, footwear, etc.)',
 'Train Manufacturing','AI','Big Data and Analytics','Cloud Computing',
 'Cybersecurity','E-Commerce','Gaming and Entertainment','IT Services',
 'Metavers','Networking','Robotics','Software and Services',
 'Virtual Reality','Building Products','Cement and Concrete','Chemicals',
 'Construction materials','Containers and Packaging','Glass and Ceramics',
 'Paper and Forest products','Coal mining','Copper Mining',
 'Diamond and Gemstone Mining','Metal ore mining',
 'Non-metallic mineral mining','Phosphate Mining','Potash Mining',
 'Quarrying','Rare Earth Elements Mining','Uranium Mining','Equity REITs',
 'Land Development and Agriculture','Property Management',
 'Real Estate Brokerage and Agencies','Real Estate Development',
 'Accommodation','Adventure Tourism and Recreation','Attractions',
 'Events and Conferences','Food and Beverage','Hotels and Lodging',
 'Tourism Marketing and Research','Tourism Services',
 'Transportation Services','Travel Trade','Aviation Services',
 'Freight Transportation','Logistics Services',
 'Maritime and Port Services','Parcel and Postal Services',
 'Passenger Transportation','Transportation Technology',
 'Trucking and Fleet Management','Electric Utilities','Gas Utilities',
 'Nuclear Utilities','Renewable Utilities','Waste Management',
 'Water Utilities']

sub_sectors = ['الإنتاج والتوزيع الزراعي',
"الآلات والمعدات الزراعية","الخدمات الزراعية"
,"تكنولوجيا الزراعة","تربية الحيوانات","إنتاج المحاصيل"
,"الأسمدة","صيد الأسماك (الصيد التجاري وتربية الأحياء المائية)"
,"الغابات (إنتاج الأخشاب، إنتاج اللب والورق)"
,"المزارع المتكاملة","الري وإدارة المياه"
,"الزراعة العضوية","إنتاج وتطوير البذور والوراثة"
,"الزراعة المستدامة","إنتاج الدرنات","الإعلان"
,"خدمة البيانات والإنترنت"
,"الترفيه (دور السينما، المتنزهات، الفرق الرياضية)"
,"الوسائط والخدمات التفاعلية","معلومات محتوى الإنترنت"
,"أبحاث السوق","الإعلام","خدمات الطباعة","العلاقات العامة"
,"النشر","خدمات الاتصالات","منتجات الأطفال والرضع"
,"المتاجر الكبرى","تجارة التجزئة للمواد الغذائية والسلع الأساسية","محلات البقالة"
,"المنتجات المنزلية","منتجات العناية الشخصية","الأطعمة المتخصصة"
,"المتاجر المتخصصة","منتجات التبغ"
,"التدريب والتطوير المؤسسي"
,"التعليم والرعاية في مرحلة الطفولة المبكرة (ECEC)","المراكز التعليمية"
,"المنتجات التعليمية/النشر"
,"خدمات الدعم التعليمي (أي خدمات الاختبار والاستشارات وما إلى ذلك)"
,"التعليم العالي","مدارس اللغات والاختبارات الإعدادية","المدارس الابتدائية"
,"المدارس الثانوية","التعليم والتعلم الذكي"
,'الإسكان والخدمات الطلابية','التعليم المهني والتقني'
,"الوقود البديل","طاقة الكتلة الحيوية","طاقة الفحم"
,"نقل الكهرباء/النقل والتخزين"
,"الطاقة الحرارية الأرضية","الطاقة الكهرومائية","إنتاج بطاريات الليثيوم"
,"التنقيب عن النفط والغاز","معدات وخدمات النفط والغاز"
,"تكرير النفط والغاز وتسويقهما وإنتاجهما"
,"تخزين ونقل النفط والغاز","الطاقة الشمسية","طاقة الرياح"
,"البنوك","السندات","العملات المشفرة","التكنولوجيا المالية","التأمين"
,"خدمات الاستثمار / إدارة الأصول"
,"صناديق الاستثمار العقاري (REITs)","إدارة المخاطر","سوق الأوراق المالية"
,"التكنولوجيا الحيوية","العيادات","توزيع الرعاية الصحية"
,"معدات ومستلزمات الرعاية الصحية","المستشفيات","الرعاية المدارة طويلة الأجل"
,"المختبرات الطبية","الرعاية النفسية","الأدوية"
, 'التأهيل والعلاج الطبيعي','الخدمات البيطرية'
,"الطيران والدفاع","صناعة الطائرات"
,"تصنيع السيارات","معدات الكابلات والأقمار الصناعية"
,"التشييد والهندسة (بناء وصيانة البنية التحتية مثل الطرق والجسور والمباني)"
,"صناعة المعدات الكهربائية","صناعة الإلكترونيات"
,"الصناعة البيئية","المعادن المصنعة"
,"إنتاج الأغذية والمشروبات"
,"الآلات (الصناعية والزراعة والبناء)"
,"صناعات تكنولوجيا النانو","السكك الحديدية","صناعة بناء السفن"
,"تصنيع السيليكا"
,"صناعة المنسوجات والملابس (الأقمشة والملابس والأحذية وغيرها)"
,"تصنيع القطارات","الذكاء الاصطناعي","البيانات الضخمة والتحليلات","الحوسبة السحابية"
,"الأمن السيبراني","التجارة الإلكترونية","الألعاب والترفيه","خدمات تكنولوجيا المعلومات"
,"Metavers","الشبكات","الروبوتات","البرامج والخدمات"
,"الواقع الافتراضي","منتجات البناء","الاسمنت والخرسانة","المواد الكيميائية"
,"مواد البناء","الحاويات والتغليف","الزجاج والسيراميك"
,"منتجات الورق والغابات","تعدين الفحم","تعدين النحاس"
,"تعدين الماس والأحجار الكريمة تعدين خام المعادن"
,"تعدين المعادن اللافلزية","تعدين الفوسفات","تعدين البوتاس"
,"استخراج الحجارة","استخراج العناصر الأرضية النادرة","تعدين اليورانيوم","صناديق الاستثمار العقاري"
,"تنمية الأراضي والزراعة","إدارة الممتلكات"
,'الوساطة العقارية والتوكيلات','التطوير العقاري'
,"الإقامة","سياحة المغامرات والترفيه","المعالم السياحية"
,"الفعاليات والمؤتمرات","الأطعمة والمشروبات","الفنادق والإقامة"
,"التسويق والأبحاث السياحية","الخدمات السياحية"
,"خدمات النقل","تجارة السفر","خدمات الطيران"
,"نقل البضائع","الخدمات اللوجستية"
,"الخدمات البحرية وخدمات الموانئ","الخدمات البريدية والطرود"
,"نقل الركاب","تكنولوجيا النقل"
,"النقل بالشاحنات وإدارة الأسطول","المرافق الكهربائية","مرافق الغاز"
,"المرافق النووية","المرافق المتجددة","إدارة النفايات"
,'مرافق المياه']
expected_data_types_en_for_sub = {'main_sector':sqlalchemy.types.VARCHAR(250),
                            'subsector':sqlalchemy.types.VARCHAR(250), 
                            'available':sqlalchemy.types.INTEGER}

expected_data_types_for_sub = {'القطاع_الرئيسي':sqlalchemy.types.VARCHAR(250), 
                                    'القطاع_الفرعي':sqlalchemy.types.VARCHAR(250), 
                                    'متاح':sqlalchemy.types.INTEGER}

def recommendation(recommendation):
    text = recommendation
    text1 = text.replace("@", "<br>").replace("=", "</b>").replace("+", '<b>').replace("GOLD", '<b style="color: #cfb53b">').replace("RED", '<b style="color: #e53d33">').replace("YELLOW", '<b style="color: #fcda21">').replace("GREEN", '<b style="color: #53b04d">').replace("ORANGE", '<b style="color: #f1801d">').replace("BLUE", '<b style="color: #29abe2">')
    text2 = f'<pre>{text1}</pre>'
    return text2


import csv
def update_csv(table,data):
    # df =pd.read_csv(f"{table}.csv")
    # df = df.append(data, ignore_index=True)
    # df.to_csv(f'{table}.csv',index = False, encoding= 'utf-8-sig')
    # with open(f"{table}.csv", mode='a', newline='') as file:
        # Read existing data
    existing_data = []
    with open(f"{table}.csv", mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            existing_data.append(row)

    # Append the new list to the existing data
    existing_data.append(data)

    # Write the entire updated data back to the CSV file
    with open(f"{table}.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)



if page == "Add Country":
    st.header("Add Country")

    # Allow the user to select a table to insert data
    table_to_insert = st.selectbox("Select Table",
                                   ["country_info", "economy_kpi", "funding_sources", "investment_kpi",
                                    "investmentclimate_kpi", "political_kpi","recommendation","investment_opportunities"])
    # Input field for the country name
    table_to_insert_en = table_to_insert + '_en'

    # Create two columns
    col1, col2 = st.columns(2)
    new_country_name = col1.text_input("الدولة", "")
    new_country_name_en = col2.text_input("country", "")

    # Read the columns of the selected table
    columns = read_data_from_db(table_to_insert).columns
    columns_en = read_data_from_db(table_to_insert_en).columns

    # Create input fields for each column, excluding "country"
    column_values = {}
    column_values_en = {}
    for column, column_en in zip(columns, columns_en):
        if column != "الدولة" or column_en != "country":                
            if column in columns_to_convert_to_million:
                col1, col2 = st.columns(2)
                with col1:
                    unit = st.selectbox(f"{column}", ["مليون", "مليار", "تريليون"])
                with col2:
                    entered_value = st.text_input(f"{column}", "")
                    if entered_value:
                        try:
                            converted_value = convert_to_million(entered_value, unit)
                        except Exception as e:
                            st.error(f"An error occurred: {e}\n تحقق من القيمة المدخلة")
                    else:
                        converted_value = None
                column_values_en[column_en] = converted_value
                column_values[column] = converted_value
            elif column in columns_to_convert_to_billion:
                col1, col2 = st.columns(2)
                with col1:
                    unit = st.selectbox(f"{column}", ["مليار", "مليون", "تريليون"])
                with col2:
                    entered_value = st.text_input(f"{column}", "")
                    if entered_value:
                        try:
                            converted_value = convert_to_billion(entered_value, unit)
                        except Exception as e:
                            st.error(f"An error occurred: {e}\n تحقق من القيمة المدخلة")
                    else:
                        converted_value = None
                column_values_en[column_en] = converted_value
                column_values[column] = converted_value
            elif column in precentage_col:
                if column in ['النتيجة','التوصية']: 
                    col1, col2 = st.columns(2)
                    with col1:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        tt = input_container.text_area(f"{column}:", "", height=200)
                        formatted_text = recommendation(tt)
                        st.markdown(f'<div style="direction: rtl;">{formatted_text}</div>', unsafe_allow_html=True)
                        column_values[column] = tt
                    with col2:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        tten = input_container.text_area(f"{column_en}:", "", height=200)
                        formatted_text_en = recommendation(tten)
                        st.markdown(f'<div style="direction: ltr;">{formatted_text_en}</div>', unsafe_allow_html=True)
                        column_values_en[column_en] = tten
                elif column in ['القطاع','القطاع_الفرعي']:
                    col1, col2 = st.columns(2)
                    with col1:
                        if column == 'القطاع':
                            sec = st.selectbox('القطاع:', options=main_sectors)
                            column_values[column] = sec
                        elif column == 'القطاع_الفرعي':
                            subsec = st.selectbox('القطاع الفرعي:', options=sub_sectors)
                            column_values[column] = subsec
                    with col2:
                        if column_en == 'sector':
                            sec_en = st.selectbox('sector:', options=main_sectors_en)
                            column_values_en[column_en] = sec_en
                        elif column_en == 'subsector':
                            subsec_en = st.selectbox('subsector:', options=sub_sectors_en)
                            column_values_en[column_en] = subsec_en
                elif column in ['إيرادات_الموازنة_العامة','إيرادات_الناتج_المحلي_الإجمالي','نفقات_الموازنة_العامة','فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)','فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)',
                              'أبرز_الصادرات','أبرز_الواردات']:
                    col1, col2 = st.columns(2)
                    with col1:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        column_values[column] = input_container.text_area(f"{column}:", "", height=200)
                    with col2:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        column_values_en[column_en] = input_container.text_area(f"{column_en}:", "", height=200)
                elif column in ['القطاع_الفرعي']:
                    col1, col2 = st.columns(2)
                    with col1:
                        sub = st.text_input(f"{column}", "")
                        column_values[column] = sub
                        subtable = read_data_from_db('available_investments')
                        if sub in subtable['القطاع_الفرعي'].to_list():
                            subtable.loc[subtable['القطاع_الفرعي'] == sub, 'متاح'] = 1
                            subtable.to_sql("available_investments", con=engine, if_exists='replace', index=False , dtype=expected_data_types_for_sub)
                    with col2:
                        sub_en = st.text_input(f"{column_en}", "")
                        column_values_en[column_en] = sub_en
                        subtable_en = read_data_from_db('available_investments_en')
                        if sub_en in subtable_en['subsector'].to_list():
                            subtable_en.loc[subtable_en['subsector'] == sub_en, 'available'] = 1
                            subtable_en.to_sql("available_investments_en", con=engine, if_exists='replace', index=False , dtype=expected_data_types_en_for_sub)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        column_values[column] = st.text_input(f"{column}", "")
                    with col2:
                        column_values_en[column_en] = st.text_input(f"{column_en}", "")
            else:
                per_value = st.text_input(f"{column}", "")
                per_value = per_value.replace('%', '')
                column_values_en[column_en] = per_value
                column_values[column] = per_value

    # Button to insert a row
    if st.button("Insert Country"):
        # Check if the country name and all fields are filled
        if (new_country_name and all(column_values.values())) and (
                new_country_name_en and all(column_values_en.values())):
            # Read data from the selected table
            data = read_data_from_db(table_to_insert)
            data_en = read_data_from_db(table_to_insert_en)

            # Create a new DataFrame with the row to append
            new_row = pd.DataFrame({"الدولة": [new_country_name], **column_values})
            new_row_en = pd.DataFrame({"country": [new_country_name_en], **column_values_en})

            # Concatenate the original DataFrame with the new row
            data = pd.concat([data, new_row], ignore_index=True)
            data_en = pd.concat([data_en, new_row_en], ignore_index=True)

            # Update the data in the selected table
            new_data, new_table_name, new_expected_dtypes = update_data_in_db(data, table_to_insert)
            new_data_en, new_table_name_en, new_expected_dtypes_en = update_data_in_db_en(data_en, table_to_insert_en)

            if table_to_insert not in ["economy_kpi", "investment_kpi","economy_kpi_en", "investment_kpi_en","investment_opportunities","investment_opportunities_en"] :
                try:
                    # update_csv(table_to_insert,new_data)
                    new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
                    Q = text(f"ALTER TABLE {new_table_name} ADD PRIMARY KEY (الدولة);")
                    with engine.connect() as conn:
                        conn.execute(Q)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
                    
                try:
                    # update_csv(table_to_insert_en,new_data_en)
                    new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
                    Q = text(f"ALTER TABLE {new_table_name_en} ADD PRIMARY KEY (country);")
                    with engine.connect() as conn:
                        conn.execute(Q)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
            else:
                try:
                    # update_csv(table_to_insert,new_data)
                    new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
                try:
                    # update_csv(table_to_insert_en,new_data_en)
                    new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')



            st.success(f"Added data for {new_country_name} to the {table_to_insert} table.")
            st.success(f"Added data for {new_country_name_en} to the {table_to_insert_en} table.")
            
        else:
            st.error("الرجاء ادخال جميع الحقول ,بما فيهم اسم الدولة")
            st.error("Please fill in all fields, including the country name.")

update_year = None  # Initialize update_year outside the conditionals
update_year_en = None

update_sector = None  # Initialize update_year outside the conditionals
update_sector_en = None

update_sub_sector = None  # Initialize update_year outside the conditionals
update_sub_sector_en = None

if page == "Update Country":
    st.header("Update Country")

    # Allow the user to select a table to update data
    table_to_update = st.selectbox("Select Table",
                                   ["country_info", "economy_kpi", "funding_sources", "investment_kpi",
                                    "investmentclimate_kpi", "political_kpi","recommendation","investment_opportunities"])

    table_to_update_en = table_to_update + '_en'

    # Dropdown to select the country for updating
    data = read_data_from_db(table_to_update)
    data_en = read_data_from_db(table_to_update_en)
    
    col1, col2 = st.columns(2)
    update_country = col1.selectbox("اختار الدولة التي تريد التعديل عليها:", set(data["الدولة"].tolist()))
    update_country_en = col2.selectbox("select country:", set(data_en["country"].tolist()))

    # Check if the selected table requires a year selection
    if (table_to_update in ["economy_kpi", "investment_kpi"]) and (
            table_to_update_en in ["economy_kpi_en", "investment_kpi_en"]):
        available_years = data[data["الدولة"] == update_country]["السنة"].unique()
        if available_years.any():
            update_year = st.selectbox("اختار السنة", available_years)

            
    if (table_to_update in ["investment_opportunities"]) and (
            table_to_update_en in ["investment_opportunities_en"]):
        available_sector = data[data["الدولة"] == update_country]["القطاع"].unique()
        available_sector_en = data_en[data_en["country"] == update_country_en]["sector"].unique()
        if available_sector.any() and available_sector_en.any() :
            col1, col2 = st.columns(2)
            update_sector = col1.selectbox("اختار القطاع", available_sector)
            update_sector_en = col2.selectbox("select sector", available_sector_en)
            available_sub_sector = data[(data["الدولة"] == update_country) & (data["القطاع"] == update_sector)]["القطاع_الفرعي"].unique()
            available_sub_sector_en = data_en[(data_en["country"] == update_country_en) & (data_en["sector"] == update_sector_en)]["subsector"].unique()
            if available_sub_sector.any() and available_sub_sector_en.any() :
                col1, col2 = st.columns(2)
                update_sub_sector = col1.selectbox("اختار القطاع الفرعي", available_sub_sector)
                update_sub_sector_en = col2.selectbox("select subsector", available_sub_sector_en)
            

    # Get the data for the selected row (country and year if available)
    if update_year is not None:
        selected_row = data[(data["الدولة"] == update_country) & (data["السنة"] == update_year)].iloc[0]
        selected_row_en = data_en[(data_en["country"] == update_country_en) & (data_en["year"] == update_year)].iloc[0]
    elif update_sector is not None and update_sector_en is not None:
        selected_row = data[(data["الدولة"] == update_country) & (data["القطاع"] == update_sector)].iloc[0]
        selected_row_en = data_en[(data_en["country"] == update_country_en) & (data_en["sector"] == update_sector_en)].iloc[0]
    else:
        selected_row = data[data["الدولة"] == update_country].iloc[0]
        selected_row_en = data_en[data_en["country"] == update_country_en].iloc[0]


    # Display input fields for each column, excluding "country" and "year" if not available
    column_values = {}
    column_values_en = {}
    for column, column_en in zip(data, data_en):
        if ((column != "الدولة" and (
                column != "السنة" or table_to_update not in ["economy_kpi", "investment_kpi"])) and (
                column_en != "country" and (
                column_en != "year" or table_to_update_en not in ["economy_kpi_en", "investment_kpi_en"]))) and (
                (column != "الدولة" and (
                column not in ["القطاع","القطاع_الفرعي"] or table_to_update not in ["investment_opportunities"])) and (
                column_en != "country" and (
                column_en not in ["sector","subsector"] or table_to_update_en not in ["investment_opportunities_en"]))):
            
            if column in columns_to_convert_to_million:
                col1, col2 = st.columns(2)
                with col1:
                    unit = st.selectbox(f"{column}", ["مليون", "مليار", "تريليون"])
                with col2:
                    entered_value = st.text_input(f"{column}", selected_row[column])
                    if entered_value:
                        try:
                            converted_value = convert_to_million(entered_value, unit)
                        except Exception as e:
                            st.error(f"An error occurred: {e}\n تحقق من القيمة المدخلة")
                    else:
                        converted_value = None
                column_values_en[column_en] = converted_value
                column_values[column] = converted_value
            elif column in columns_to_convert_to_billion:
                col1, col2 = st.columns(2)
                with col1:
                    unit = st.selectbox(f"{column}", ["مليار", "مليون", "تريليون"])
                with col2:
                    entered_value = st.text_input(f"{column}", selected_row[column])
                    if entered_value:
                        try:
                            converted_value = convert_to_billion(entered_value, unit)
                        except Exception as e:
                            st.error(f"An error occurred: {e}\n تحقق من القيمة المدخلة")
                    else:
                        converted_value = None
                column_values_en[column_en] = converted_value
                column_values[column] = converted_value
            elif column in precentage_col:
                if column in ['النتيجة','التوصية']: 
                    col1, col2 = st.columns(2)
                    with col1:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        tt = input_container.text_area(f"{column}:", selected_row[column], height=200)
                        formatted_text = recommendation(tt)
                        st.markdown(f'<div style="direction: rtl;">{formatted_text}</div>', unsafe_allow_html=True)
                        column_values[column] = tt
                    with col2:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        tten = input_container.text_area(f"{column_en}:", selected_row_en[column_en], height=200)
                        formatted_text_en = recommendation(tten)
                        st.markdown(f'<div style="direction: ltr;">{formatted_text_en}</div>', unsafe_allow_html=True)
                        column_values_en[column_en] = tten
                elif column in ['إيرادات_الموازنة_العامة','إيرادات_الناتج_المحلي_الإجمالي','نفقات_الموازنة_العامة','فرص_الاستثمار_المتاحة/قطاعات_(كما_تعلنها_الدولة)','فرص_الاستثمار_المتاحة_(حسب_التقارير_المتخصصة)',
                              'أبرز_الصادرات','أبرز_الواردات']:
                    col1, col2 = st.columns(2)
                    with col1:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        column_values[column] = input_container.text_area(f"{column}:", selected_row[column], height=200)
                    with col2:
                        # Create a Streamlit container and apply custom CSS to control the size
                        input_container = st.container()
                        # Add the text input box using st.text_area
                        column_values_en[column_en] = input_container.text_area(f"{column_en}:", selected_row_en[column_en], height=200)
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        column_values[column] = st.text_input(f"{column}", selected_row[column])
                    with col2:
                        column_values_en[column_en] = st.text_input(f"{column_en}", selected_row_en[column_en])
            else:
                per_value = st.text_input(f"{column}", selected_row[column])
                if per_value:
                    per_value = per_value.replace('%', '')
                column_values_en[column_en] = per_value
                column_values[column] = per_value

    # Button to update a row based on the selected country
    if st.button("Update Country Data"):
        # Check if the selected country exists in the data
        if (update_country in data["الدولة"].tolist()) and (update_country_en in data_en["country"].tolist()):
            for (column, value), (column_en, value_en) in zip(column_values.items(), column_values_en.items()):
                if update_year is not None:
                    data.loc[(data["الدولة"] == update_country) & (data["السنة"] == update_year), column] = value
                    data_en.loc[(data_en["country"] == update_country_en) & (
                    data_en["year"] == update_year), column_en] = value_en
                elif update_sector is not None and update_sub_sector is not None:
                    data.loc[(data["الدولة"] == update_country) & (data["القطاع"] == update_sector) & (data["القطاع_الفرعي"] == update_sub_sector), column] = value
                    data_en.loc[(data_en["country"] == update_country_en) & (
                    data_en["sector"] == update_sector_en) & (data_en["subsector"] == update_sub_sector_en), column_en] = value_en
                else:
                    data.loc[data["الدولة"] == update_country, column] = value
                    data_en.loc[data_en["country"] == update_country_en, column_en] = value_en

            # Update the data in the selected table
            new_data, new_table_name, new_expected_dtypes = update_data_in_db(data, table_to_update)
            new_data_en, new_table_name_en, new_expected_dtypes_en = update_data_in_db_en(data_en, table_to_update_en)





            if table_to_update not in ["economy_kpi", "investment_kpi","economy_kpi_en", "investment_kpi_en","investment_opportunities","investment_opportunities_en"] :
                try:
                    # update_csv(table_to_insert,new_data)
                    new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
                    Q = text(f"ALTER TABLE {new_table_name} ADD PRIMARY KEY (الدولة);")
                    with engine.connect() as conn:
                        conn.execute(Q)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
                try:
                    # update_csv(table_to_insert_en,new_data_en)
                    new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
                    Q = text(f"ALTER TABLE {new_table_name_en} ADD PRIMARY KEY (country);")
                    with engine.connect() as conn:
                        conn.execute(Q)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
            else:
                try:
                    # update_csv(table_to_insert,new_data)
                    new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')
                try:
                    # update_csv(table_to_insert_en,new_data_en)
                    new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
                except Exception as e:
                    st.error(f'Error occurred while updating data: {str(e)}')





            if update_year is not None:
                st.success(f"Updated data for {update_country} in the {table_to_update} table for year {update_year}.")
                st.success(
                    f"Updated data for {update_country_en} in the {table_to_update_en} table for year {update_year}.")
            else:
                st.success(f"Updated data for {update_country} in the {table_to_update} table.")
                st.success(f"Updated data for {update_country_en} in the {table_to_update_en} table.")

    # Display the selected row's data
    with st.sidebar:
        if update_year is not None:
            st.subheader(f"Data for {update_country} in {update_year}:")
            st.subheader(f"Data for {update_country_en} in {update_year}:")
        else:
            st.subheader(f"Data for {update_country}:")
        st.write(
            data[(data["الدولة"] == update_country) & (data["السنة"] == update_year)] if update_year is not None else
            data[data["الدولة"] == update_country])
        st.write(data_en[(data_en["country"] == update_country_en) & (
                    data_en["year"] == update_year)] if update_year is not None else data_en[
            data_en["country"] == update_country_en])



# if page == "Add Available Investments":
#     st.header("Add Available Investments")


#     available_investments_table = "available_investments"
#     available_investments_table_en = available_investments_table + '_en'
    
#     d = read_data_from_db(available_investments_table)
#     dn = read_data_from_db(available_investments_table_en)

#     # Read the columns of the selected table
#     columns = read_data_from_db(available_investments_table).columns
#     columns_en = read_data_from_db(available_investments_table_en).columns

#     col1, col2 = st.columns(2)
#     update_main_sector = col1.selectbox("اختار القطاع الرئيسي الذي  تريد ادخاله:", set(d["القطاع_الرئيسي"].tolist()))
#     update_main_sector_en = col2.selectbox("select main sector:", set(dn["main_sector"].tolist()))

    
#     # Create input fields for each column
#     column_values = {}
#     column_values_en = {}
#     for column, column_en in zip(columns, columns_en):
#             if column in ['القطاع_الفرعي']: 
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     # Create a Streamlit container and apply custom CSS to control the size
#                     input_container = st.container()
#                     # Add the text input box using st.text_area
#                     column_values[column] = input_container.text_area(f"{column}:", "", height=200)
#                 with col2:
#                     # Create a Streamlit container and apply custom CSS to control the size
#                     input_container = st.container()
#                     # Add the text input box using st.text_area
#                     column_values_en[column_en] = input_container.text_area(f"{column_en}:", "", height=200)
#             elif column in ['متاح']:
#                 per_value = st.selectbox("متاح",["Yes","No"])
#                 if per_value == "Yes":
#                     bool_avail = 1
#                 else:
#                     bool_avail = 0
#                 column_values_en[column_en] = bool_avail
#                 column_values[column] = bool_avail
#     # Button to insert a row
#     if st.button("Insert Data"):
#             # Read data from the selected table
#             data = read_data_from_db(available_investments_table)
#             data_en = read_data_from_db(available_investments_table_en)

#             # Create a new DataFrame with the row to append
#             new_row = pd.DataFrame({"القطاع_الرئيسي": [update_main_sector], **column_values})
#             new_row_en = pd.DataFrame({"main_sector": [update_main_sector_en], **column_values_en})

#             # Concatenate the original DataFrame with the new row
#             data = pd.concat([data, new_row], ignore_index=True)
#             data_en = pd.concat([data_en, new_row_en], ignore_index=True)

#             # Update the data in the selected table
#             new_data, new_table_name, new_expected_dtypes = update_data_in_db(data, available_investments_table)
#             new_data_en, new_table_name_en, new_expected_dtypes_en = update_data_in_db_en(data_en, available_investments_table_en)

#             try:
#                 new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
#             except Exception as e:
#                 st.error(f'Error occurred while updating data: {str(e)}')
#             try:
#                 new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
#             except Exception as e:
#                 st.error(f'Error occurred while updating data: {str(e)}')



#             st.success(f"Added data to the {available_investments_table} table.")
#             st.success(f"Added data to the {available_investments_table_en} table.")



# update_s_sector = None
# update_s_sector_en = None

# if page == "Update Available Investments":
#     st.header("Update Available Investments")

#     available_investments_update = "available_investments"
#     available_investments_update_en = available_investments_update + '_en'


#     d = read_data_from_db(available_investments_update)
#     dn = read_data_from_db(available_investments_update_en)

#     col1, col2 = st.columns(2)
#     u_main_sector = col1.selectbox("اختار القطاع الرئيسي الذي  تريد التعديل عليه:", set(d["القطاع_الرئيسي"].tolist()))
#     u_main_sector_en = col2.selectbox("select main sector:", set(dn["main_sector"].tolist()))


#     u_subsector = d[d["القطاع_الرئيسي"] == u_main_sector]["القطاع_الفرعي"].unique()
#     u_subsector_en = dn[dn["main_sector"] == u_main_sector_en]["subsector"].unique()
#     if u_subsector.any() and u_subsector_en.any() :
#         col1, col2 = st.columns(2)
#         update_s_sector = col1.selectbox("اختار القطاع الفرعي", u_subsector)
#         update_s_sector_en = col2.selectbox("select sub-sector", u_subsector_en)



#     # Get the data for the selected row (country and year if available)
#     if update_s_sector is not None and update_s_sector_en is not None:
#         selected_row = d[(d["القطاع_الرئيسي"] == u_main_sector) & (d["القطاع_الفرعي"] == update_s_sector)].iloc[0]
#         selected_row_en = dn[(dn["main_sector"] == u_main_sector_en) & (dn["subsector"] == update_s_sector_en)].iloc[0]



#     column_values = {}
#     column_values_en = {}
#     for column, column_en in zip(d, dn):
#         if column in ['القطاع_الرئيسي','القطاع_الفرعي']: 
#             col1, col2 = st.columns(2)
#             with col1:
#                 # Create a Streamlit container and apply custom CSS to control the size
#                 input_container = st.container()
#                 # Add the text input box using st.text_area
#                 column_values[column] = input_container.text_area(f"{column}:", selected_row[column], height=20)
#             with col2:
#                 # Create a Streamlit container and apply custom CSS to control the size
#                 input_container = st.container()
#                 # Add the text input box using st.text_area
#                 column_values_en[column_en] = input_container.text_area(f"{column_en}:", selected_row_en[column_en], height=20)
#         elif column in ['متاح']:
#             per_value = st.selectbox("متاح",["Yes","No"])
#             if per_value == "Yes":
#                 bool_avail = 1
#             else:
#                 bool_avail = 0
#             column_values_en[column_en] = bool_avail
#             column_values[column] = bool_avail

#     # Button to insert a row
#     if st.button("Update Data"):
#         if (u_main_sector in d["القطاع_الرئيسي"].tolist()) and (u_main_sector_en in dn["main_sector"].tolist()):
#             for (column, value), (column_en, value_en) in zip(column_values.items(), column_values_en.items()):
#                 if update_s_sector is not None and update_s_sector_en is not None:
#                     d.loc[(d["القطاع_الرئيسي"] == u_main_sector) & (d["القطاع_الفرعي"] == update_s_sector), column] = value
#                     dn.loc[(dn["main_sector"] == u_main_sector_en) & (
#                     dn["subsector"] == update_s_sector_en), column_en] = value_en
#                 else:
#                     d.loc[d["القطاع_الرئيسي"] == u_main_sector, column] = value
#                     dn.loc[dn["main_sector"] == u_main_sector_en, column_en] = value_en

#             # Update the data in the selected table
#             new_data, new_table_name, new_expected_dtypes = update_data_in_db(d, available_investments_update)
#             new_data_en, new_table_name_en, new_expected_dtypes_en = update_data_in_db_en(dn, available_investments_update_en)

#             try:
#                 new_data.to_sql(new_table_name, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes)
#             except Exception as e:
#                 st.error(f'Error occurred while updating data: {str(e)}')
#             try:
#                 new_data_en.to_sql(new_table_name_en, con=engine, if_exists='replace', index=False, dtype=new_expected_dtypes_en)
#             except Exception as e:
#                 st.error(f'Error occurred while updating data: {str(e)}')



#             # st.success(f"Added data to the {available_investments_table} table.")
#             # st.success(f"Added data to the {available_investments_table_en} table.")
#             if update_s_sector is not None:
#                 st.success(f"Updated data for {u_main_sector} in the {available_investments_update} table for year {update_s_sector}.")
#                 st.success(
#                     f"Updated data for {u_main_sector_en} in the {available_investments_update_en} table for year {update_s_sector_en}.")
#             else:
#                 st.success(f"Updated data for {u_main_sector} in the {available_investments_update} table.")
#                 st.success(f"Updated data for {u_main_sector_en} in the {available_investments_update_en} table.")

        # # Display the selected row's data
        # with st.sidebar:
        #     if update_year is not None:
        #         st.subheader(f"Data for {update_country} in {update_year}:")
        #         st.subheader(f"Data for {update_country_en} in {update_year}:")
        #     else:
        #         st.subheader(f"Data for {update_country}:")
        #     st.write(
        #         data[(data["الدولة"] == update_country) & (data["السنة"] == update_year)] if update_year is not None else
        #         data[data["الدولة"] == update_country])
        #     st.write(data_en[(data_en["country"] == update_country_en) & (
        #                 data_en["year"] == update_year)] if update_year is not None else data_en[
        #         data_en["country"] == update_country_en])





# Display the selected table's data from the database
if page == "Add Country":
    data = read_data_from_db(table_to_insert)
    data_en = read_data_from_db(table_to_insert_en)
elif page == "Update Country":
    data = read_data_from_db(table_to_update)
    data_en = read_data_from_db(table_to_update_en)
# elif page == "Add Available Investments":
#     data = read_data_from_db(available_investments_table)
#     data_en = read_data_from_db(available_investments_table_en)
# elif page == "Update Available Investments":
#     data = read_data_from_db(available_investments_update)
#     data_en = read_data_from_db(available_investments_update_en)
with st.sidebar:
    if page == "Add Country":
        st.subheader(f"{table_to_insert} Data:")
        st.write(data)
        st.subheader(f"{table_to_insert_en} Data:")
        st.write(data_en)
    elif page == "Update Country":
        st.subheader(f"{table_to_update} Data:")
        st.write(data)
        st.subheader(f"{table_to_update_en} Data:")
        st.write(data_en)
    # elif page == "Add Available Investments":
    #     st.subheader(f"{available_investments_table} Data:")
    #     st.write(data)
    #     st.subheader(f"{available_investments_table_en} Data:")
    #     st.write(data_en)
    # elif page == "Update Available Investments":
    #     st.subheader(f"{available_investments_update} Data:")
    #     st.write(data)
    #     st.subheader(f"{available_investments_update_en} Data:")
    #     st.write(data_en)

# Assuming available_investments_table and available_investments_table_en are defined somewhere before this code snippet

# Display the selected table's data from the database
# data = read_data_from_db(table_to_insert if page == "Add Country" else table_to_update)
# data_en = read_data_from_db(table_to_insert_en if page == "Add Country" else table_to_update_en)
# available_investments_data = read_data_from_db(available_investments_table if page == "Add Available Investments" else available_investments_table_en)
# available_investments_data_en = read_data_from_db(available_investments_table_en if page == "Add Available Investments" else available_investments_table)

# with st.sidebar:
#     st.subheader(f"{table_to_insert if page == 'Add Country' else table_to_update} Data:")
#     st.write(data)
#     st.subheader(f"{table_to_insert_en if page == 'Add Country' else table_to_update_en} Data:")
#     st.write(data_en)
#     st.subheader(f"{available_investments_table if page == 'Add Available Investments' else available_investments_table_en} Data:")
#     st.write(available_investments_data)
#     st.subheader(f"{available_investments_table_en if page == 'Add Available Investments' else available_investments_table} Data:")
#     st.write(available_investments_data_en)

