#!/usr/bin/env python
# coding: utf-8

# # Исследование надежности заемщиков





# ## Откройте таблицу и изучите общую информацию о данных

# ** 1. Импортируйте библиотеку pandas. Считайте данные из csv-файла в датафрейм и сохраните в переменную `data`. Путь к файлу:**
#
# `/datasets/data.csv`

# In[3]:


import pandas as pd

try:
    data = pd.read_csv('/datasets/data.csv')
except:
    data = pd.read_csv('https://code.s3.yandex.net/datasets/data.csv')


# **2. Выведите первые 20 строчек датафрейма `data` на экран.**

# In[4]:


data.head(20)


# ** 3. Выведите основную информацию о датафрейме с помощью метода `info()`.**

# In[5]:


data.info()


# ## Предобработка данных

# ### Удаление пропусков

# **4. Выведите количество пропущенных значений для каждого столбца. Используйте комбинацию двух методов.**

# In[6]:


data.isna().sum()


# **5. В двух столбцах есть пропущенные значения. Один из них — `days_employed`. Пропуски в этом столбце вы обработаете на следующем этапе. Другой столбец с пропущенными значениями — `total_income` — хранит данные о доходах. На сумму дохода сильнее всего влияет тип занятости, поэтому заполнить пропуски в этом столбце нужно медианным значением по каждому типу из столбца `income_type`. Например, у человека с типом занятости `сотрудник` пропуск в столбце `total_income` должен быть заполнен медианным доходом среди всех записей с тем же типом.**

# In[7]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['total_income'].isna()), 'total_income'] = \
    data.loc[(data['income_type'] == t), 'total_income'].median()


# ### Обработка аномальных значений

# **З 6. В данных могут встречаться артефакты (аномалии) — значения, которые не отражают действительность и появились по какой-то ошибке. таким артефактом будет отрицательное количество дней трудового стажа в столбце `days_employed`. Для реальных данных это нормально. Обработайте значения в этом столбце: замените все отрицательные значения положительными с помощью метода `abs()`.**

# In[8]:


data['days_employed'] = data['days_employed'].abs()


# **7. Для каждого типа занятости выведите медианное значение трудового стажа `days_employed` в днях.**

# In[9]:


data.groupby('income_type')['days_employed'].agg('median')


# У двух типов (безработные и пенсионеры) получатся аномально большие значения. Исправить такие значения сложно, поэтому оставьте их как есть.

# **8. Выведите перечень уникальных значений столбца `children`.**

# In[10]:


data['children'].unique()


# ** 9. В столбце `children` есть два аномальных значения. Удалите строки, в которых встречаются такие аномальные значения из датафрейма `data`.**

# In[11]:


data = data[(data['children'] != -1) & (data['children'] != 20)]


# ** 10. Ещё раз выведите перечень уникальных значений столбца `children`, чтобы убедиться, что артефакты удалены.**

# In[12]:


data['children'].unique()


# ### Удаление пропусков (продолжение)

# ** 11. Заполните пропуски в столбце `days_employed` медианными значениями по каждого типа занятости `income_type`.**

# In[13]:


for t in data['income_type'].unique():
    data.loc[(data['income_type'] == t) & (data['days_employed'].isna()), 'days_employed'] = \
    data.loc[(data['income_type'] == t), 'days_employed'].median()


# ** 12. Убедитесь, что все пропуски заполнены. Проверьте себя и ещё раз выведите количество пропущенных значений для каждого столбца с помощью двух методов.**

# In[14]:


data.isna().sum()


# ### Изменение типов данных

# ** 13. Замените вещественный тип данных в столбце `total_income` на целочисленный с помощью метода `astype()`.**

# In[15]:


data['total_income'] = data['total_income'].astype(int)


# ### Обработка дубликатов

# ** 14. Обработайте неявные дубликаты в столбце `education`. В этом столбце есть одни и те же значения, но записанные по-разному: с использованием заглавных и строчных букв. Приведите их к нижнему регистру.**

# In[16]:


data['education'] = data['education'].str.lower()


# ** 15. Выведите на экран количество строк-дубликатов в данных. Если такие строки присутствуют, удалите их.**

# In[17]:


data.duplicated().sum()


# In[18]:


data = data.drop_duplicates()


# ### Категоризация данных

# ** 16. На основании диапазонов, указанных ниже, создайте в датафрейме `data` столбец `total_income_category` с категориями:**
# 
# - 0–30000 — `'E'`;
# - 30001–50000 — `'D'`;
# - 50001–200000 — `'C'`;
# - 200001–1000000 — `'B'`;
# - 1000001 и выше — `'A'`.
# 
# 
# **Например, кредитополучателю с доходом 25000 нужно назначить категорию `'E'`, а клиенту, получающему 235000, — `'B'`. Используйте собственную функцию с именем `categorize_income()` и метод `apply()`.**

# In[19]:


def categorize_income(income):
    try:
        if 0 <= income <= 30000:
            return 'E'
        elif 30001 <= income <= 50000:
            return 'D'
        elif 50001 <= income <= 200000:
            return 'C'
        elif 200001 <= income <= 1000000:
            return 'B'
        elif income >= 1000001:
            return 'A'
    except:
        pass


# In[20]:


data['total_income_category'] = data['total_income'].apply(categorize_income)


# ** 17. Выведите на экран перечень уникальных целей взятия кредита из столбца `purpose`.**

# In[21]:


data['purpose'].unique()


# ** 18. Создайте функцию, которая на основании данных из столбца `purpose` сформирует новый столбец `purpose_category`, в который войдут следующие категории:**
# 
# - `'операции с автомобилем'`,
# - `'операции с недвижимостью'`,
# - `'проведение свадьбы'`,
# - `'получение образования'`.
# 
# **Например, если в столбце `purpose` находится подстрока `'на покупку автомобиля'`, то в столбце `purpose_category` должна появиться строка `'операции с автомобилем'`.**
# 
# **Используйте собственную функцию с именем `categorize_purpose()` и метод `apply()`. Изучите данные в столбце `purpose` и определите, какие подстроки помогут вам правильно определить категорию.**

# In[22]:


def categorize_purpose(row):
    try:
        if 'автом' in row:
            return 'операции с автомобилем'
        elif 'жил' in row or 'недвиж' in row:
            return 'операции с недвижимостью'
        elif 'свад' in row:
            return 'проведение свадьбы'
        elif 'образов' in row:
            return 'получение образования'
    except:
        return 'нет категории'


# In[23]:


data['purpose_category'] = data['purpose'].apply(categorize_purpose)
print(data)


# ### Шаг 3. Исследуйте данные и ответьте на вопросы

# #### 3.1 Есть ли зависимость между количеством детей и возвратом кредита в срок?

# Для решения данного вопроса необходимо найти общее количество заемщиков для каждой группы по количеству детей, 
# количество должников в каждой группе и их долю от общего количества заемщиков.
# 

# In[24]:


# Cоздадим сводную таблицу для столбца children  по значению долга (debt). 
# Подсчитаем общее количество заемщиков для каждой категории (count)
# и сколько заемщиков в каждой категории имеют долг (sum).Проверим полученный результат:


# Вариант 1:

# addiction_kids_refund = data.pivot_table(index='children', values='debt', aggfunc=['count', 'sum'])# Ваш код будет здесь. Вы можете создавать новые ячейки.
# addiction_kids_refund   

# Вариант 2:

# (в отличии от варианта 1 позволяет создать новый столбец на основе полученных данных:)
# addiction_kids_refund_group = data.groupby('children').agg(total_count=('debt','count'), total_debt=('debt','sum', 'mean'))

addiction_kids_refund_group = data.groupby('children').agg(total_count=('debt','count'), total_debt=('debt','sum'), avg_debt=('debt','mean'))
print(addiction_kids_refund_group.sort_values(by='avg_debt', ascending=False))


# In[25]:


# Вычислим долю количества должников на общее количество заемщиков с разным количеством детей:
addiction_kids_refund_group['debt_fraction_with_children'] = addiction_kids_refund_group['total_debt'] / addiction_kids_refund_group['total_count']

# Отсортируем полученные данные по доле должников и выведем их в порядке убывания:
print(addiction_kids_refund_group.sort_values(by='debt_fraction_with_children', ascending=False))


# Рассчитаем относительный % между максимальной и минимальной долей группы должников, 
# которую проверяем на зависимость между количеством детей и возвратом кредита в срок:   

# In[27]:


value1 = 0.097561
value2 = 0.075438

relative_percentage = ((value1 - value2) / value2) * 100

print(relative_percentage)



# **Вывод:** Исходя из полученных данных, нет конкретной зависимости в порядке убывания/прибывания количества детей. 
#     Наименьшая доля должников среди заемщиков, не имеющих детей. Далее идут заемщики с 1 и 2 детьми. 
#     Данные по заемщикам с 5, 3 и 4 детьми набрали еще не достаточное количество для анализа и потребуют со временем 
#     повторного просмотра. Вычисление относительного процента между максимальной и минимальной долей группы должников показывает, что разница составляет 29,33%. Это может указывать на то, что количество детей может влиять на вероятность возникновения долга у заемщиков, но необходимо учитывать и другие факторы, такие как уровень дохода, кредитный рейтинг и другие обстоятельства.
# 
# В целом, для более точного анализа и вывода о зависимости между количеством детей и возвратом кредита в срок, необходимо расширить выборку данных и учитывать другие связанные факторы.



# #### 3.2 Есть ли зависимость между семейным положением и возвратом кредита в срок?

# In[24]:


#Приведем все данные столбца 'family_status' в нижний регистр:
data['family_status'] = data['family_status'].str.lower()


# In[25]:


# Подсчитаем общее количество заемщиков для каждой категории семейного положения (count)
# и сколько заемщиков в каждой категории имеют долг (sum). Проверим полученные значения:

dependence_status_group = data.groupby('family_status').agg(total_count_status=('debt','count'), total_debt_status=('debt','sum')).reset_index()
dependence_status_group 
# Ваш код будет здесь. Вы можете создавать новые ячейки.


# In[26]:


# Вычислим долю количества должников на общее количество заемщиков с семейным статусом:
dependence_status_group['debt_fraction'] = dependence_status_group['total_debt_status'] / dependence_status_group['total_count_status']

# Отсортируем полученные данные по доле должников и выведем их в порядке убывания:
print(dependence_status_group.sort_values(by='debt_fraction', ascending=False))


#  **Вывод:** Исходя из полученных данных, заемщики с семейным статусом "Не женат / не замужем" и "гражданский брак" имеют самую высокую долю долгов.Анализ данных по семейному положению и возврату кредита в срок выявил следующие тенденции:
# 
# 1.Заемщики, состоящие в гражданском браке, имеют самую высокую долю должников (385 из 4134), что составляет 9,31%.
# 2.Заемщики, состоящие в браке, занимают второе место по доле должников (927 из 12261), составляя 7,56%.
# 3.Заемщики, не состоящие в браке (не женатые/не замужем), имеют третью по величине долю должников (273 из 2796), составляя 9,76%.
# 3.Заемщики, находящиеся в разводе, имеют наименьшую долю должников (84 из 1189), составляя 7,06%.
# 4.Вдовы/вдовцы занимают последнее место по доле должников (63 из 951), составляя 6,62%.
# 
# **Объяснение:**
# 
# В целом, можно сказать, что заемщики, состоящие в браке или гражданском браке, имеют более высокую долю должников по сравнению с заемщиками, не состоящими в браке. Это может быть связано с тем, что заемщики, могут быть более склонны к заключению кредитов для покрытия дополнительных расходов на возросшие потребности и цели.
# 
# Также стоит отметить, что заемщики, находящиеся в разводе или являющиеся вдовцами, имеют относительно низкую долю должников. Это может быть связано с тем, что они могут быть более осторожными в своих финансовых решениях из-за изменений в их семейном положении и финансовой ситуации.
# 
# Однако, стоит отметить, что эти данные могут быть связаны с другими факторами, такими как возраст, уровень дохода и тд. Например, заемщики, состоящие в браке или гражданском союзе, могут быть в среднем старше, иметь более высокий уровень дохода по сравнению с заемщиками, не состоящими в браке. Это может объяснить, почему они имеют более высокую долю должников.
# 
# В целом, для более точного анализа и вывода о зависимости между семейным положением и возвратом кредита в срок, необходимо расширить выборку данных и учитывать другие связанные факторы.




# #### 3.3 Есть ли зависимость между уровнем дохода и возвратом кредита в срок?

# Для решения данного вопроса необходимо найти общее количество заемщиков для каждого уровня дохода, 
# количество должников в каждой группе и их долю от общего количества заемщиков.

# In[ ]:


# выведем разброс доходов, так табличка будет выглядеть информативней:
def levels_categorize_income(income):
    try:
        if 0 <= income <= 30000:
            return 'до 30000'
        elif 30001 <= income <= 50000:
            return 'от 30000 до 50000'
        elif 50001 <= income <= 200000:
            return 'от 50000 до 200000'
        elif 200001 <= income <= 1000000:
            return 'от 200000 до 1000000'
        elif income >= 1000001:
            return 'более 1000000'
    except:
        pass
    
data['levels_income_category'] = data['total_income'].apply(levels_categorize_income)
print(data)


# In[36]:


# Подсчитаем общее количество заемщиков для каждой категории уровня дохода (count)
# и сколько заемщиков в каждой категории имеют долг (sum). Выведем полученный результат:

borrowers_income_group = data.groupby('levels_income_category').agg(total_borrowers_income=('debt','count'), debt_borrowers_income=('debt','sum')).reset_index()
borrowers_income_group 
# Ваш код будет здесь. Вы можете создавать новые ячейки.



# In[37]:


# Вычислим долю количества должников на общее количество заемщиков с семейным статусом:
borrowers_income_group['debt_fraction_income'] = borrowers_income_group['total_borrowers_income'] / borrowers_income_group['debt_borrowers_income']


# Отсортируем полученные данные по доле должников и выведем их в порядке убывания:
print(borrowers_income_group.sort_values(by='debt_fraction_income', ascending=False))
 



# **Вывод:** Более широкие данные даны по категории с доходом 'C', которые стоят на втором месте по убыванию доли не возврата кредита в срок. Данная целевая аудитория считается более предпочтительной. Категории 'E' имеет наименьшую долю, но данные еще требуют проверки после того, как наберется больше статистики. Данные по категории 'C' также предоставлены пока в минимальном количестве. Категории 'B' и 'D' имеют наибольшую долю долгов.

# #### 3.4 Как разные цели кредита влияют на его возврат в срок?

# Для решения данного вопроса необходимо найти общее количество заемщиков для каждой категории цели кредита, 
# количество должников в каждой группе и их долю от общего количества заемщиков.

# In[29]:


# Подсчитаем общее количество заемщиков для каждой категории (count)
# и сколько заемщиков в каждой категории имеют долг (sum). Выведем полученный результат:

purpose_loan_group = data.groupby('purpose_category').agg(total_purpose_loan=('debt','count'), debt_purpose_loan=('debt','sum')).reset_index()
purpose_loan_group 
# Ваш код будет здесь. Вы можете создавать новые ячейки.


# In[30]:


# Вычислим долю количества должников на общее количество заемщиков по целям кредита:
purpose_loan_group['debt_fraction_purpose'] = purpose_loan_group['total_purpose_loan'] / purpose_loan_group['debt_purpose_loan']


# Отсортируем полученные данные по доле должников и выведем их в порядке убывания:
print(purpose_loan_group.sort_values(by='debt_fraction_purpose', ascending=False))# Ваш код будет здесь. Вы можете создавать новые ячейки.


# **Вывод:** Исходя из полученных данных, меньше всего доля должников по кредиту - среди категорий: 'операции с автомобилем', 'получение образования'.  А наибольшая среди категорий: 'операции с недвижимостью'  и 'проведение свадьбы'.

# #### 3.5 Возможные причины появления пропусков в исходных данных.

# *Ответ:* Среди возможных причин можно отметить: 
# 
# а) Человеческий фактор. Человеческий фактор может включать много разных вариантов: перепутанные категориальные и количественные переменные, числа, не верно записанные переменные, пропуски, отсутствие данных и много др.
# 
# б) Технологические ошибки. Ошибки, которые можно обработать с помощью try/except (ошибки при считывании данных, копировании и тд). 


# Пропущенные значения в столбце days_employed:
# 
# Возможно, это связано с тем, что информация о количестве рабочих дней не была указана для всех заемщиков. Некоторые заемщики могли не хотеть раскрывать эту информацию или она просто не была доступна.
# Это может влиять на точность анализа данных.
# 
# Пропущенные значения в столбце total_income:
# 
# Пропуски в данных о доходах могут быть связаны с тем, что некоторые заемщики не хотят раскрывать свою финансовую информацию или она просто не была доступна.
# Заполнение пропущенных значений медианными значениями по типу занятости позволяет уменьшить влияние пропущенных значений на анализ данных. В целом, пропущенные значения могут повлиять на точность анализа данных и привести к искажению результатов. Поэтому перед проведением анализа следует тщательно изучить причины пропусков и,  возможно, запросить их. Или, скорее всего тут ошибка на стороне банка (Человеческая или Техническая),  потому что скорее всего заявку банк даже не будет рассматривать Если в ней не указан доход

# #### 3.6 Почему заполнить пропуски медианным значением — лучшее решение для количественных переменных.

# *Ответ:* Медианное значение позволяет разделить отсортированный список пополам, так как в списке могут содержаться единичные значения, которые очень далеки от среднего.


# ### Шаг 4: общий вывод.

# Данное исследование показало, что зависимость возврат кредита в срок зависит от категории должников по семейному положению и уровню дохода. А так же от количества детей в семье, но не пропорционально их количеству. Однако в некоторых категориях каждого исследования, есть такие, где количество заемщиков составляет очень малое число и исследование по данным группам потребуют доработки, когда соберется достаточное количество заемщиков данной группы.






