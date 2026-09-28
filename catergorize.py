import pandas as pd

# 1. Read CSV
df = pd.read_csv('ehealth_reviews.csv')
df['content'] = df['content'].fillna('')

# 5.data cleaning!
df['content']=df['content'].str.strip()

blacklist = ['好', '差', '很好', '很差', '好差', '不错', '还行', '垃圾',
             'good', 'bad', 'ok', 'fine', 'great', 'terrible', 'nice', 'shit','too bad','Rubbish']

df = df[~df['content'].str.contains('|'.join(blacklist), na=False)]
df = df[df['content'].str.len() >= 6] #delete strings <6

print(f"after data cleaning, {len(df)}left")


# 2. Define categories with English labels and cantonese and mandering
keywords = {
    'Registration/Login Issues': [
        '注册', '登记', '登录', '登入', '身份验证', '密码', 
        'register', 'login', 'sign up', 'password', 'verify', 'authentication','密碼'
    ],
    'Forced Updates': [
        '更新', '強制', '强制', '更新后', '不能使用', 
        'update', 'force', 'upgrade', 'mandatory'
    ],
    'UI/Navigation Issues': [
        '界面', '畫面', '功能', '找不到', '难用', '难找', '混乱', '麻煩',
        'interface', 'navigation', 'hard to use', 'customize', 'menu', 'confusing','UIUX'
    ],
    'Missing Features': [
        '缺少', '沒有', '没有', '功能少', '不全', 
        'missing', 'lack', 'no feature', 'feature request','唔到','優化'
    ],
    'Performance/Crashes': [
        '闪退', '閃退', '卡顿', '崩溃', '慢', '開啟','开启','連線','更新','long time',
        'crash', 'lag', 'freeze', 'slow', 'bug', 'glitch','loading','cannot get it to work','load',"can't open"
    ],
}

# 3. Auto-categorize 
def categorize(text):
    text = str(text).lower()
    for category, words in keywords.items():
        for word in words:
            if word in text:
                return category
    # Check for positive feedback if no negative keyword matches
    if any(pos in text for pos in ['好', '方便','容易使用','有用', 'good', 'easy', 'useful', 'helpful', 'love']):
        return 'Positive Feedback'
    return 'Other'

df['Category'] = df['content'].apply(categorize)


counts = df['Category'].value_counts()
print("Category Counts:\n", counts)
print("\nPercentage:\n", df['Category'].value_counts(normalize=True).round(2) * 100)


df.to_csv('ehealth_reviews_classified.csv', index=False, encoding='utf-8-sig')
print("\nSaved as ehealth_reviews_classified.csv")