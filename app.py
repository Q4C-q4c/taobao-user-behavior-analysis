import streamlit as st
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import Pie

st.set_page_config(page_title="一亿条淘宝用户行为分析",layout="wide")
st.title("一亿条淘宝用户行为分析")

jobs=[
    ("data/热销商品榜.csv"),
    ("data/流量商品榜.csv"),
    ("data/流量类目榜.csv"),
    ("data/热销类目榜.csv"),
    ("data/类目前十与长尾的pv和buy总占比情况.csv"),
    ("data/9天各行为的数量.csv"),
    ("data/24小时各行为的数量.csv"),
    ("data/唯一加购数,加购转化率和数据时间长度.csv"),
    ("data/加购后发生购买的不同时间长度占比.csv"),
    ("data/21,22,23点加购之后24小时之内的购买情况.csv"),
    ("data/总用户数,总活跃天数,平均活跃天数.csv"),
    ("data/连续登录占比.csv"),
    ("data/去除连续登录大于8天的用户后剩余人的平均活跃天数.csv"),
    ("data/不同pv量级的数量,转化率,0成交占比.csv"),
    ("data/商品复购率.csv"),
    ("data/回头客率.csv"),
    ("data/类目的回购率.csv"),
    ("data/数据清洗前不同年份下的数据量.csv")
]

@st.cache_data
def load_data():
    dfs = {}
    for job in jobs:
        table_name = job.rsplit('.',1)[0].split('/',1)[1]
        dfs[table_name] = pd.read_csv(job,encoding="utf-8-sig")
    return dfs

dfs=load_data()
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["热门热销","时间维度","连续登录","转化率","复购","数据导入与清洗","索引与中间表的建立"])


def onechart(name,x,y1,y2,titles):   #表名,id,购买,浏览,标题
    cols1,cols2=st.columns(2)
    with cols1:
        st.dataframe(dfs [name])
    with cols2:
        ids=dfs[name][x].tolist()
        buys=dfs[name][y1].tolist()
        pvs=dfs[name][y2].tolist()
        rates=dfs[name]["rate"].tolist()
        ids=[str(i) for i in ids]
        bar=Bar(init_opts=opts.InitOpts(width="100%")) #跟随器，用于消除滚动条
        bar.add_xaxis(ids)
        bar.add_yaxis("购买量",buys)
        bar.add_yaxis("浏览量",pvs)
        bar.extend_axis(yaxis=opts.AxisOpts(name="转化率(%)",position="right"))
        line=Line()
        line.add_xaxis(ids)
        line.add_yaxis("转化率",rates,yaxis_index=1)
        bar.overlap(line)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title=titles),
            legend_opts=opts.LegendOpts()
        )
        st.iframe(bar.render_embed())

def onechart2(x,y,z):  #那一列，区域名字，标题
    groups=dfs['类目前十与长尾的pv和buy总占比情况']['group_name'].tolist()
    pcts=dfs['类目前十与长尾的pv和buy总占比情况'][x].tolist()
    pairs=[]
    for g,p in zip(groups,pcts):
        pairs.append([g,p])
    pie=Pie(init_opts=opts.InitOpts(width="100%"))  #跟随器，用于消除滚动条
    pie.add(y,pairs)
    pie.set_global_opts(
            title_opts=opts.TitleOpts(title=f"前十类目与长尾的{z}占比情况"),
            legend_opts=opts.LegendOpts()
                )
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
    st.iframe(pie.render_embed())

def twochart(name,x):   #表名，时间
    st.dataframe(dfs[name])
    pvs=dfs[name]['pv'].tolist()
    buys=dfs[name]['buy'].tolist()
    times=dfs[name][x].tolist()
    favs=dfs[name]['fav'].tolist() 
    carts=dfs[name]['cart'].tolist()
    line = Line(init_opts=opts.InitOpts(width="100%"))  #跟随器，用于消除滚动条
    line.add_xaxis(times)
    line.add_yaxis("浏览",pvs)
    line.extend_axis(yaxis=opts.AxisOpts(name="次数",position="right"))
    line.add_yaxis("购买",buys,yaxis_index=1)
    line.add_yaxis("收藏",favs,yaxis_index=1)
    line.add_yaxis("加购",carts,yaxis_index=1)
    line.set_global_opts(
            title_opts=opts.TitleOpts(title=name),
            legend_opts=opts.LegendOpts()
        )
    st.iframe(line.render_embed())


with tab1:
    onechart("热销商品榜","item_id","buy","pv","热销前十商品榜")
    onechart("流量商品榜","item_id","buy","pv","流量前十商品榜")
    onechart("热销类目榜","category_id","buy_cnt","pv_cnt","热销前十类目榜")
    onechart("流量类目榜","category_id","buy_cnt","pv_cnt","流量前十类目榜")

    st.dataframe(dfs["类目前十与长尾的pv和buy总占比情况"])
    cols1,cols2=st.columns(2)
    with cols1:
        onechart2("pv_pct","pv占比","pv")
    with cols2:
        onechart2("buy_pct","buy占比","buy")
    with st.container(horizontal=True):
        st.subheader("结论：")
        st.markdown("通过商品和类目热销款和曝光款前十榜单得知，商品两榜单的重合度是1/10，同时可按流量与转化率分为三类：有利润款，代表为只在热销款且为榜首的3122135，其转化率为1,408 ÷ 1779 ≈ 79.15%。也有大爆款，代表为两榜单都在的3031354，转化率为950 ÷ 17,169 ≈ 5.5%。还有引流款，代表为只在热门款的812879，转化率为136/30079≈0.45%，远低于平均转化率2.25%。类目两榜单的重合度则有5/10，其结构虽没有爆款类目（没有曝光与转化双高的类目），但也能重演为引流与利润两种。这其中，重合的 5个类目转化率全部低于均值（0.63%~1.42%），靠百万级流量硬上热销榜；而热销前三则是不在流量榜的中等流量类目，转化率3.02%~5.06%，是利润类目。最后再通过计算可得，头部10 类目吃掉 28% 流量但只贡献 9.6%购买（0.77%），长尾（10名外）转化率 却有2.83% ，是前十的 3.7 倍。")
    

with tab2:
    twochart("9天各行为的数量","day")
    with st.expander("一 日走势：预热，蓄水"):
        st.markdown("从“9天各行为的数量”的总体来看，11-25到11-30 平稳，12-01到12-02大幅度上升，而后12-03基本维持数量。在大幅度的上升中：pv +26.9%、fav +29.2%、加购 +27.3%、购买 +22.8%；较前 7 日均值，加购+40.2%、pv +32.6%、fav +32.3%、购买 +20.3%。12-02和12-03相比同为周六周日的11-25和11-26，前者四种行为的数量都显著高于后者，说明这种爆发增长的成因不是周末效应而是双12预热带来的。同时四种行为中cart(加购)上升尤为明显，购买则处于垫底状态，这可以得出，在双12的预热下是意图先堆积、购买跟进较慢，呈蓄水型。")
        
    twochart("24小时各行为的数量","hour")
    with st.expander("二 时段分布：21 点流量峰、04 点谷底、白天高原"):
        st.markdown("由“24小时各行为的数量”图和数据可得pv 峰值 21:00(753.8 万)，谷底 04:00(45.0 万)，相差 16.8 倍；白天 10-18 点维持 420-480 万/小时的高峰。因此推荐的运营路线是，晚上作为流量主战场，白天作为稳定基本盘。而04 点前后因流量极低，则适合安排系统维护与功能测试。")
    with st.expander("三 时段转化：上午 10 点为转化峰值，与流量峰镜像"):
        st.markdown("由“24小时各行为的数量”图表得，buy_rate 峰值是10:00(2.95%)，谷底是05:00(1.40%)；与 pv 峰值(21:00)相距 11小时，pv与buy_rate整体负相关——流量最大的时段转化最弱，流量中等的时段转化最强。再从大致时段来看，白天转化率为2.13-3.0%，而晚间则降至 1.4-2.03%。接着细看晚上的数据，可以得知22点的cart(486249) 一路升至全天最高，buy_rate同时下降——夜间“浏览→加购”走得多，但“加购→购买”走得少。最后得出白天转化高、晚间流量大转化低，因此平台应白天给利润款+大爆款推流，晚间给引流款+大爆款推流。")
    line = Line(init_opts=opts.InitOpts(width="100%"))
    hours=dfs["24小时各行为的数量"]["hour"].tolist()
    buy_rates=dfs["24小时各行为的数量"]["buy_rate"].tolist()
    cart_rates=dfs["24小时各行为的数量"]["cart_rate"].tolist()
    line.add_xaxis(hours)
    line.add_yaxis("转化率",buy_rates)
    line.add_yaxis("加购率",cart_rates)
    line.set_global_opts(
            yaxis_opts=opts.AxisOpts(name="%"),
            title_opts=opts.TitleOpts(title="24小时转化率和加购率"),
            legend_opts=opts.LegendOpts()
            )
    st.iframe(line.render_embed())
    
    row=dfs["唯一加购数,加购转化率和数据时间长度"].iloc[0]   #单行表，取唯一那一行
    cnt=row["cnt"]
    buy_rate=row["buy_rate"]
    duration=row["time"]
    with st.container(horizontal=True):
        st.metric("唯一加购数",f"{int(cnt):,}",border=True)
        st.metric("加购转化率",f"{buy_rate:.2f}%",border=True)
        st.metric("数据时间长度",f"{int(duration)}小时",border=True)

    st.dataframe(dfs["加购后发生购买的不同时间长度占比"])
    df=dfs["加购后发生购买的不同时间长度占比"]  
    order=["0-8","8-16","16-24","24-32","32-40","40-48","48-72","72+"]   
    gap_to_rate=dict(zip(df["time_gap"],df["b_rate"]))   
    time_gaps=order
    b_rates=[gap_to_rate[g] for g in order]
    bar = Bar(init_opts=opts.InitOpts(width="100%"))
    bar.add_xaxis(time_gaps)
    bar.add_yaxis("占比",b_rates)
    bar.set_global_opts(
                title_opts=opts.TitleOpts(title="加购后发生购买的不同时间长度占比"),
                legend_opts=opts.LegendOpts(),
                yaxis_opts=opts.AxisOpts(name="%")
            )
    st.iframe(bar.render_embed())

    st.dataframe(dfs["21,22,23点加购之后24小时之内的购买情况"])
    b_hours=dfs["21,22,23点加购之后24小时之内的购买情况"]["b_hour"].tolist()
    h_rates=dfs["21,22,23点加购之后24小时之内的购买情况"]["h_rate"].tolist()
    pairs = sorted(zip(b_hours,h_rates))
    b_hours=[p[0] for p in pairs]
    h_rates=[p[1] for p in pairs]
    line = Line(init_opts=opts.InitOpts(width="100%"))
    line.add_xaxis(b_hours)
    line.add_yaxis("占比",h_rates)
    line.set_global_opts(
                title_opts=opts.TitleOpts(title="21,22,23点加购之后24小时之内的购买情况"),
                legend_opts=opts.LegendOpts(),
                yaxis_opts=opts.AxisOpts(name="%")
            )
    st.iframe(line.render_embed())
    with st.expander("四 间隔分布：当夜密度高 ，次日平铺，得出“次日早晨集中兑现”这个说法不成立"):
        st.markdown("由“加购后发生购买的不同时间长度占比”的图表并计算可以得出窗口内总兑现率约6.79%，即93.2% 的加购对窗口内未兑现。其次还能得出兑现者的间隔分布：8 小时内 27.5%(1.87/6.79)、8-24 小时 30.3%(2.06/6.79)、24 小时以上42%(2.85/6.79)——“推迟”在天的尺度上真实存在，与日走势的蓄水型结论相符。然后来到“21,22,23点加购之后24小时之内的购买情况”这对图表，可以看出的是用户在夜间加购之后当晚的3小时内的购买占24小时的37%，密度最高，为密度峰值；次日白天段(08-15)：0.57%，占24小时购买的约44%，总量大于当晚。最后，通过计算当晚和次日白天两段大致对半，因此可以推出“推迟到次日早晨集中兑现”的说法不成立。")
    with st.expander("五 局限"):
        st.markdown("类目与商品均为匿名编号，无法解释品类属性；双 12 在窗口外，蓄水的最终兑现不可验证；93.2% 未兑现加购的归宿(放弃 vs推迟)无法区分。")

with tab3:
    row=dfs["总用户数,总活跃天数,平均活跃天数"].iloc[0]   #单行表，取唯一那一行
    total_user=row["total_user"]
    total_active_days=row["total_active_days"] 
    avg_active_days=row["avg_active_days"]
    row2=dfs["去除连续登录大于8天的用户后剩余人的平均活跃天数"].iloc[0]
    avg_no8=row2["avg_days"]
    with st.container(horizontal=True):
        st.metric("总用户数",f"{int(total_user):,}",border=True)
        st.metric("总活跃天数",f"{int(total_active_days):,}天",border=True)
        st.metric("平均活跃天数",f"{avg_active_days:.2f}天",border=True)    
        st.metric("去除连登≥8天用户后的平均活跃天数",f"{avg_no8:.2f}天",delta=f"{avg_no8-avg_active_days:.2f}天",delta_color="off",border=True)

    st.dataframe(dfs["连续登录占比"])
    df1=dfs["连续登录占比"]
    labels=[c.replace("pct_","")+ "天" for c in df1.columns]
    pcts=df1.iloc[0].tolist()
    bar = Bar(init_opts=opts.InitOpts(width="100%"))
    bar.add_xaxis(labels)
    bar.add_yaxis("占比",pcts,itemstyle_opts=opts.ItemStyleOpts(color="#FF9500"))
    bar.set_global_opts(
                title_opts=opts.TitleOpts(title="连续登录占比"),
                legend_opts=opts.LegendOpts(),
                yaxis_opts=opts.AxisOpts(name="%")
            )
    st.iframe(bar.render_embed())
    with st.container(horizontal=True):
        st.subheader("结论：")
        st.markdown("连续登录两天及以上的客户占总客户数的99.51%，相比根据平均活跃7.05天算出的最低占比51%（p × 9 + (1−p) × 5 = 7.05），高出近两倍，说明这近100万的客户，大多数用户都是活跃用户而非一次性用户。再看到多个连续登录的占比99.51(≥2)->87.45(≥3)->71.1(≥4)->43.19(≥6)->29.66(≥8)，该曲线是连续纯度曲线，不是流失曲线，下降趋势为：3到4下降16%——最陡，6到8平均1天掉7%——最缓，整体是先陡后缓的，整体趋势是健康正常的。再然后去掉连续登录≥8(29.66%)的用户，剩下七成的用户平均登陆天数也有6.29天，可以看出用户粘性很高，该软件的用户粘性已经不是短板。由前面的数据可得曝光前十类目只有0.77%的转化率，十名之外的类目有2.83%的转化率，销量最高的商品，转化率有79.15%，但其曝光度却在10名开外，同时随着曝光度的上升(pv)，转化率也开始下降，pv<5平均转化率为2.86%，pv>=500平均转化率为1.97%。因此，运营的重心应从“泛曝光”转向“精准分发”：将更多精准流量（搜索结果、个性化推荐）分配给高转化商品，同时保留引流款的引流职能。")
with tab4:
    st.dataframe(dfs["不同pv量级的数量,转化率,0成交占比"])
    df2=dfs["不同pv量级的数量,转化率,0成交占比"]
    cols1,cols2=st.columns(2)
    pvs=df2["pv"].tolist()
    cnts=df2["cnt"].tolist()
    avg_rates=df2["avg_rate"].round(2).tolist()
    zero_pcts=df2["0_pct"].round(2).tolist()
    with cols1:
        line = Line(init_opts=opts.InitOpts(width="100%"))
        line.add_xaxis(pvs)
        line.add_yaxis("平均转化率",avg_rates)
        line.extend_axis(yaxis=opts.AxisOpts(name="%",position="right"))
        line.add_yaxis("0成交占比",zero_pcts,yaxis_index=1)
        line.set_global_opts(
                    title_opts=opts.TitleOpts(title="不同pv量级的转化率,0成交占比"),
                    legend_opts=opts.LegendOpts(),
                    yaxis_opts=opts.AxisOpts(name="%")
                )
        st.iframe(line.render_embed())
    with cols2:
        bar = Bar(init_opts=opts.InitOpts(width="100%"))
        bar.add_xaxis(pvs)
        bar.add_yaxis("数量",cnts,itemstyle_opts=opts.ItemStyleOpts(color="#B700FF"))
        bar.set_global_opts(
                    title_opts=opts.TitleOpts(title="不同pv量级的数量"),
                    legend_opts=opts.LegendOpts()
                )
        st.iframe(bar.render_embed())
    with st.container(horizontal=True):
        st.subheader("结论：")
        st.markdown("由按pv数分层统计零成交占比和平均转化率的表，首先可以得知的是，随着pv的上升，cnt2453186->22939——pv 不足 5 次的商品有 245 万个，是 ≥500 的 100多倍，长尾才是商品池的大头。然后可以得到，随着pv的上升平均转化率 2.86% →1.97%。而后，再从类目榜得知，流量排行前十的类目只有0.77%转化率，其余类目的平均转化率则达到2.83%。从这些图表不难看出，商品的转化率会随着pv(浏览)数的上升而下降，这是因为随着pv的上升，零成交占比 95.6% → 5.0%，商品至少卖出一件的概率从 4.4% 飙升到 95.0%，且pv数越高，引流款占比越大，pv数较低的，用户越可能是搜索/推荐精准直达，转化反而高，导致不同的pv数，转化率分布随pv数系统性漂移。也因此pv不存在单一稳定门槛，应分不同层次统计。")

with tab5:
    names=["商品复购率","回头客率","类目的回购率"]
    dfa=[dfs[n] for n in names]
    dfb=pd.concat(dfa,axis=0,ignore_index=True)
    dfb.insert(0,"name",names)
    dfb=dfb.sort_values(by="rate",ascending=False)
    dfb.columns = ["指标","产生购买的用户数","复购数","占比（%）"]
    st.dataframe(dfb,hide_index=True)
    with st.container(horizontal=True):
        st.subheader("结论：")
        st.markdown("由数据可得，回头客率(66.01%)及人数443,858，品类的复购率(21.87%)及人数147,078，商品的复购率(9.23%)及人数62039。占比逐渐下降，是因为筛选条件越来越严格导致每个占比的分子越来越小。" \
        "这其中有147078 - 62039 = 85,039:在类目里回购了、但没有回购同一单品的人，占品类复购客户的57.8%。" \
        "也有443,858 − 147,078 = 296,780:买了两单以上、但没在任何一个类目里回购的人，占多单用户的 66.9%——前者代表的是忠于需求的用户，后者代表的是忠于平台的用户。" \
        "但该数据有一定的局限性，类目和商品均以匿名编号表示，无法判断品类属性，因此无法解释高回购类目的成因。" \
        "最后由这些数据可以得知，该平台首先要做的就是加强推送与搜索的精确性和个性化，满足用户需求，提高品类的复购率——1.同一品类商品数量多，让用户回购的选择更多，推送多样化，2.品类回购者中 57.8%换了不同商品，单品级召回会漏掉近六成回购需求，只有把召回颗粒度从单品提升到品类，才能在保持定向的同时接住这六成。" \
        "相比之下，其中 66.9%（296,780人）在多单用户中是跨类目分散购买者——他们忠于平台而非具体类目，没有稳定的类目偏好信号，难以定向触达。而在提高商品复购率这条路上则是可用于推送的商品选择少。")

with tab6:
    with st.container(horizontal=True):   #horizontal=True决定了st.metric的排列方式，默认是垂直排列
        st.metric("数据总行数","100,150,807",border=True)
        st.metric("数据体积","3.5GB",border=True)
        st.metric("导入耗时","19分钟",border=True)
    with st.container(horizontal=True):
        st.metric("字段","user_id/item_id/category_id/behavior_type/event_time",border=True)
        st.metric("分析窗口","2017-11-25 ~ 12-03（9天）",border=True)
    with st.container():
        st.subheader("数据导入")
        st.markdown("通过使用LOAD DATA 原生批量导入的这种方法，使得1 亿行，3.5GB的csv数据最后实际耗时19分钟，相比to_sql 逐行插入预估的 3 小时，快了约 9 倍。")
    with st.container(horizontal=True):
        LD='''
            import pymysql  
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='*************',
                database='taobao',
                charset='utf8mb4',
                local_infile=True   
            )
            cursor = conn.cursor()
            cursor.execute("""
                LOAD DATA LOCAL INFILE 'C:<你的本地路径>/UserBehavior.csv'
                INTO TABLE user_behavior
                FIELDS TERMINATED BY ','
                (user_id, item_id, category_id, behavior_type, event_time)
            """)
            conn.commit()
            print("导入完成")
        '''
        st.code(LD,language="python")

    with st.container():
        st.subheader("数据清洗")
        st.markdown("按年份逐层排查，发现负时间戳（NULL 318 行）、1970 年等截断错误、窗口外数据。")
        year='''
            select
            from_unixtime(no_day*86400,'%Y') as year,
            sum(cnt) as sum
            from
            (
            select
            (event_time+28800) DIV 86400 as no_day,
            count(*) as cnt
            from user_behavior
            group by no_day
            ) t
            group by year
            order by year
        '''
        st.code(year,language="sql")
    st.dataframe(dfs["数据清洗前不同年份下的数据量"])
    with st.container():
        st.markdown("通过WHERE过滤条件，去掉负时间戳、1970 年等截断错误、窗口外数据，得到100,095,231行数据。")
        where='''
                select
                count(*) as cnt
                from user_behavior
                where event_time >= 1511539200 and event_time<1512316800;
            '''
        st.code(where,language="sql")
    with st.container(horizontal=True):
        st.subheader("数据清洗的过程与结果：")
        st.markdown("以时间维度(天)对一亿条数据进行了排查。发现负时间戳（318 行）、散布在 1970~2037 年间的 36 个异常年份（共 1,581 行），合计非 2017 数据 1,899 行。还有处于正确范围(2017-11-25到2017-12-03)外的2017-11-24和2017-12-04这类窗口外数据。这两类脏数据有55,576行占0.056%，这其中2017-11-24的数据有40,231行占脏数据总数的72%。处理方法用WHERE过滤，通过WHERE过滤后数据量为100,095,231，加55,576等于总数据100,150,807，故清洗没有错误，没有扰乱数据。")

with tab7:
    with st.container():
        st.metric("经过索引与中间表的建立后查询速度","19分37秒 → 11.1秒",delta="快约107倍",delta_color="off",border=True)
        st.subheader("索引的建立：")
        st.markdown("给五列建单列索引，服务点查类查询。")
        sy='''
                import os
                import time
                from sqlalchemy import create_engine

                engine = create_engine('mysql+pymysql://root:**********@localhost:3306/taobao?charset=utf8mb4')

                start = time.time()
                with engine.connect() as conn:
                    conn.exec_driver_sql("""
                        ALTER TABLE user_behavior
                            ADD INDEX idx_user (user_id),
                            ADD INDEX idx_item (item_id),
                            ADD INDEX idx_cate (category_id),
                            ADD INDEX idx_behavior (behavior_type),
                            ADD INDEX idx_time (event_time)
                    """)
                    conn.commit()
                print(f"索引建立完成，耗时 {time.time() - start:.0f} 秒")
            '''
        st.code(sy, language="python")

        st.subheader("中间表的建立：")
        st.markdown("**item_t（商品×类目四行为聚合）**")
        item_t=('''
            set tmp_table_size = 512 * 1024 * 1024 ;
            set max_heap_table_size=512 * 1024 * 1024 ;
            set sort_buffer_size = 128 * 1024 * 1024 ;  
            create table item_t as
            select
            item_id,
            category_id,
            count(case when behavior_type='pv' then 1 else null end) as pv_cnt,
            count(case when behavior_type='buy' then 1 else null end) as buy_cnt,
            count(case when behavior_type='cart' then 1 else null end) as cart_cnt,
            count(case when behavior_type='fav' then 1 else null end) as fav_cnt
            from user_behavior ignore index (idx_behavior, idx_item, idx_time)
            where event_time >= 1511539200 and event_time<1512316800
            group by item_id,category_id;
             ''')
        st.code(item_t,language="sql")
        st.markdown("这里忽略索引，是因为item_t 的过滤条件命中约 99.95% 的行，选择性极低，此时走索引（随机回表）反而不如全表扫描（顺序 IO）；实测对比后，用ignore index 强制全扫。")
        st.markdown("item_t 四列行为计数总和 = 100,095,231，加清洗掉的 55,576 = 总数据 100,150,807——建中间表的过程没有丢一行数据。")
        st.markdown("**user_day（用户×天去重，服务 tab3 连续登录）**")
        user_day=('''
            set tmp_table_size = 256 * 1024 * 1024 ;
            set max_heap_table_size=256 * 1024 * 1024 ;
            set sort_buffer_size = 256 * 1024 * 1024 ;  
            create table user_day as
            select
            from_unixtime(no_day*86400,'%Y-%m-%d') as day,
            user_id
            from
            (
            select
            (event_time+28800) DIV 86400 as no_day,
            user_id
            from user_behavior
            where event_time >= 1511539200 and event_time<1512316800
            group by no_day,user_id
            ) t;
            ''')
        st.code(user_day,language="sql")
        st.markdown("**item_sum（商品×pv/buy 汇总加主键，服务 tab4 分层）**")
        item_sum=('''
        create table item_sum as
        select
        item_id,
        sum(pv_cnt) as pv_sum,
        sum(buy_cnt) as buy_sum
        from item_t
        group by item_id;
        alter table item_sum add primary key (item_id);
            ''')
        st.code(item_sum,language='sql')
    st.subheader("收益与对账：")
    st.markdown("通过item_t，曝光前十商品的查询从 19 分 37 秒降到 11.1 秒，快 107 倍。提速主因是中间表：查询从对 1 亿行实时聚合，变为直接读约400万行的预聚合结果，这是空间换时间。索引则负责的是另一类查询（按用户/商品/时间的点查）。")
