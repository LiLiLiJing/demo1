###############  Notes  ###############

1. 导入本地json文件进入数据库：
	python read_into_aircraft_warship.py, 然后输入“json文件地址”。要加引号。

2. 在环球网上爬取数据并导入数据库：
	webscrap.py + data_into_mysql.py （旧版）
	new_webscrap.py （新版）
	两个版本暂时都不能直接运行，详情见下方 ## python ##部分

3. 添加相关资源：
	python find_relation.py


###############  TXT  ###############

1. aircraft.txt
	内容从军事网飞行器类抓取，为string格式，用@@隔断每个飞行器的url。共有1330个url。

2. warship.txt
	内容从军事网舰船舰艇类抓取，为string格式，用@@隔断每个舰船舰艇的url。共有1192个url。


###############  Python  ###############

1. build_data.py
	（暂无用）
	测试右侧下方关系图（鼠标移动显示节点信息）时，临时为所有links数据表表中出现的Source、Target建立一组（Files，Value，Images， Rel，Links）信息，并加入到know_graph数据表中。

2. data_to_mysql.py
	（暂无用）
	连接know_graph数据表。将webscrap.py从网页上提取到的信息进行处理，网上图片下载到本地。所有信息添加进know_graph数据表中。
	目前 max retries exceed。Header可能需要修改。

3. demonew.py 
	运行程序

4. find_relation.py
	选取know_graph数据表中所有数据，提取出所有的Entity和Value。遍历所有的Entity，将提取到的value信息split（';;'),在其他所有的value信息中做模糊查询。根据相同value信息的个数，将对应的Entity从多到少加入Rel，上限为15个。每个Entity之间用';;'隔断。

5. form_links.py 
	find（kw）：从links数据表中查找所有的Target为kw，或Source为kw的信息
	find_rela（kw，num）：num为查找的关系层数。find_rela返回所有kw的关联Entities的所有信息（Entity，Files，Value，...）
	build_rel_info(kw, num）：提取关联Entities的Value信息。

6. new_webscrap.py
	(不可直接用python new_webscrap运行）
	此文件使用python jupyter notebook写的，直接下载保存下来的。不可直接运行，需要添加encode=utf-8 等Python2所需的转码格式。而且需要分成两个.py文件分别运行。是webscrap 和 data_to_mysql 的综合版。从本地读取 aircraft.txt 和 warship.txt, 进行抓取信息。

7. read_into_aircraft_warship.py
	从json文件中读取entity、files、value等信息，加入aircraft_warship数据表中

8. read_into_links 
	从json文件中读取links信息，加入links数据表中

9. recover_json.py 
	从aircraft_warship数据表中查找entity、files, links等信息，返回json格式

10. search.py
	模糊查询，将查找到的Entity以string格式返回，Entity之间用“@”隔断。
	
11. webscarp.py
	爬虫，从环球网-军事中提取所需信息。支持分类输入，提取该分类下的所有页面的信息。


###############  Mysql  ###############

1. Database： knowgraph

2. Tables：aircraft_warship, links
	   (know_graph 无用)

3. 数据表中文乱码问题：输入 "set names latin1;" 即可正常显示

  	
