"""
1.计算求2+4+6+8+...+100的和
2.统计不同英雄的成绩
3.车型抱怨的数据统计

"""
print('homework 1:')
ret = 0
for i in range(2, 102, 2):
    ret += i
print('2+4+6+8+...+100的和是：{0}'.format(ret))

# 作业2
print('\nhomework 2:')
import pandas as pd

data = {
    '语文': [68, 95, 98, 90, 80],
    '数学': [65, 76, 86, 88, 90],
    '英语': [30, 98, 88, 77, 90]
}
df = pd.DataFrame(data, index=['张飞', '关羽', '刘备', '典韦', '许褚'])
df.index.name = '姓名'
print('原数据：')
print(df)
# 统计数据
desc = df.describe()
# 去除不需要的columns
desc.drop(index=['count', '25%', '50%', '75%'], axis=1, inplace=True)
desc.index = ['平均分', '方差', '最小值', '最大值']
print('\n统计数据：')
# 统计总分数
sum_score = df.sum(axis=1)
sum_score.name = '总分数'
merge_sum = pd.merge(df, sum_score, left_index=True, right_index=True, how='left')
merge_sum_sort = merge_sum.sort_values('总分数', ascending=False)
# 合并表格
concat = pd.concat([merge_sum_sort, desc])
print(concat.fillna('').round(decimals=2))

# 作业3
print('\n\nhomework 3:')
# 读取数据
car = pd.read_csv('./car_complain.csv')


def replace_name(name):
    if name == '一汽-大众':
        name = '一汽大众'
    return name


# 将problem列按照‘，’号进行分割
car = pd.concat([car.drop(columns=['problem']), car['problem'].str.get_dummies(',')], axis=1)
# 将品牌列数据格式统一
car['brand'] = car['brand'].apply(replace_name)
# 按品牌进行分组统计
brand_sum = car.groupby('brand').agg('count')['id']
brand_sum.name = '车型投诉总数'
df_brand = brand_sum.to_frame()
print(df_brand.sort_values('车型投诉总数', ascending=False))

# 按车型进行分组统计
car_model_sum = car.groupby('car_model').agg('count')['id']
car_model_sum.name = '品牌投诉总数'
df_car_model = car_model_sum.to_frame()
print(df_car_model.sort_values('品牌投诉总数', ascending=False))

# 按品牌及车型进行分组
car_model_sum1 = car.groupby(['brand', 'car_model'])['id'].agg('count').groupby('brand').mean()
car_model_sum1.name = '平均车型投诉总数'
mean_car_model_p = car_model_sum1.to_frame()
print(mean_car_model_p.sort_values('平均车型投诉总数', ascending=False).round(decimals=2))
