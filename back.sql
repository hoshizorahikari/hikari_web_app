-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: localhost    Database: myblog
-- ------------------------------------------------------
-- Server version	5.7.19-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blogs`
--

DROP TABLE IF EXISTS `blogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blogs` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `name` varchar(50) NOT NULL,
  `summary` varchar(200) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogs`
--

LOCK TABLES `blogs` WRITE;
/*!40000 ALTER TABLE `blogs` DISABLE KEYS */;
INSERT INTO `blogs` VALUES ('00152325317565724506cf13930463b85440bdaa6751ed0000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','娴嬭瘯鐢?,'This is a test','hello world!',1523253175.65724),('00152325624799756f824c535de47e68d60b73a92eefbb1000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','Test2','This is a summary','This is content.',1523256247.99745),('001523258664605d1716b136ed648c6b0dae4dcfdc5899d000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','娴嬭瘯鐢?,'This is summary','Hello, world!',1523258664.59723),('001523324896573896efb5508d6435cad809a2b1e517124000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','1234','no use','## Head\n----\n1. python\n2. javascript\n3. data structure\n4. database\n5. c++\n\n---\n#涓轰粈涔坢arkdown娌℃湁鏁堟灉锛?',1523324896.57338),('00152332494414558bea0b1c9f64f63988add72da3d36e7000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','111','111','111\n\n# Hello \n\n- apple\n- strawberry\n- lemon',1523324944.14563),('001523324949804ca157b70ff13477c8178ee96ef8489f4000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','222','222','222',1523324949.80494),('0015233249610970a3c5b7a38c24d60947d8663837bdc22000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','444','444','444',1523324961.0972),('001523324965992fb14dcd2544e47fc9d1f26569875ae53000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','555','555','555',1523324965.99277),('001523324971886a69e28a9e79e4784857fdfd0ec7f3957000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','666','666','666',1523324971.88626),('001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','777','777','777  \n```python\ndef show():\n    print(\'hello world\')\n\nif __name__ == \'__main__\':\n    show()\n```\n    \n```javascript\n    let a =1;\n    alert (a);\n```',1523324989.28851),('00152332499464081b91674b82c43b89391e5676cceefe2000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','888','888','888',1523324994.64032),('001523343790558461afd39709247cb8f20948f3a559d4c000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','markdown test','test','# head1\n## head2\n### head3\n----  \n#鍔犵矖#\n`寮曠敤`',1523343790.55878),('0015234322193411ceb8f42260f4fd78dbc8d099f6bf672000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','鍐掓场鎺掑簭','bubble sort','```python\ndef bubble_sort(arr):\n    for i in range(len(arr) - 1, 0, -1):\n        exchange = False\n        for j in range(i):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                exchange = True\n        if not exchange:\n            break\n```',1523432219.3414),('00152352460083879ff8260d21f4e54856cc61626d2ef24000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','aaaa','aaaa','### javascript闂寘搴旂敤涔嬪亸鍑芥暟\n```javascript\nfunction make_pow(n) {\n    return function (x) {\n        return Math.pow(x, n);\n    }\n}\n// 鍒涘缓涓や釜鍋忓嚱鏁皒2鍜寈3\nlet pow2 = make_pow(2);\nlet pow3 = make_pow(3);\nconsole.log(pow2(25)); // 625, 25鐨勫钩鏂筡nconsole.log(pow3(16)); // 4096, 16鐨勭珛鏂筡n```',1523524600.83831),('00152392775082590630711290c4cc792a411b84b9eccd2000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','瑾曠敓鏃ャ亰銈併仹銇ㄣ亞銆佹洔銇曘倱锛?,'4鏈?7鏃ャ伅娓¤竞鏇溿伄瑾曠敓鏃ワ紒','![娓¤竞鏇淽(/static/img/1445t.jpg)',1523927750.82575),('0015239281312390d49b0edc6af4a189af14029d96d4812000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','with璇彞涓庝笂涓嬫枃绠＄悊鍣?,'with璇彞涓庝笂涓嬫枃绠＄悊鍣?,'### with璇彞\nwith璇彞鐨勫熀鏈娉曠粨鏋勫涓?銆€銆€銆€\n```python\nwith expression [as variable]:\n    with-block\n```\nwith璇彞鐨別xpression鏄笂涓嬫枃绠＄悊鍣ㄣ€俓nwith璇彞鐨刐as variable]鏄彲閫夌殑锛屽鏋滄寚瀹氫簡as variable璇存槑绗︼紝鍒檝ariable鏄笂涓嬫枃绠＄悊鍣╡xpression璋冪敤\\_\\_enter\\_\\_()鍑芥暟杩斿洖鐨勫璞°€傛墍浠ワ紝f骞朵笉涓€瀹氬氨鏄痚xpression锛岃€屾槸expression.\\_\\_enter\\_\\_()鐨勮繑鍥炲€硷紝鑷充簬expression.\\_\\_enter\\_\\_()杩斿洖浠€涔堝氨鐢辫繖涓嚱鏁版潵鍐冲畾浜嗐€倃ith-block鏄墽琛岃鍙ワ紝with-block鎵ц瀹屾瘯鏃讹紝with璇彞浼氳嚜鍔ㄨ繘琛岃祫婧愭竻鐞嗭紝姣斿鑷姩鍏抽棴鏂囦欢銆俓n\n------\n\nexpression鏄竴涓笂涓嬫枃绠＄悊鍣紝鍏跺疄鐜颁簡\\_\\_enter\\_\\_鍜孿\_\\_exit\\_\\_涓や釜鍑芥暟銆傝皟鐢ㄤ竴涓獁ith璇彞鏃讹紝鎵ц杩囩▼濡備笅锛歕n1. 棣栧厛鐢熸垚涓€涓笂涓嬫枃绠＄悊鍣╡xpression锛屾瘮濡俙with open(\"1.txt\") as f:`锛岄鍏堜互\"test.txt\"浣滀负鍙傛暟鐢熸垚涓€涓笂涓嬫枃绠＄悊鍣╫pen(\"test.txt\")銆俓n2. 鐒跺悗鎵цexpression.\\_\\_enter\\_\\_()銆傚鏋滄寚瀹氫簡[as variable]璇存槑绗︼紝灏哱\_\\_enter\\_\\_()鐨勮繑鍥炲€艰祴缁檝ariable銆傚open(\"test.txt\").\\_\\_enter\\_\\_()杩斿洖鐨勬槸涓€涓枃浠跺璞＄粰f銆俓n3. 鎵цwith-block璇彞鍧椼€俓n4. 鎵цexpression.\\_\\_exit\\_\\_()锛屽湪\\_\\_exit\\_\\_()鍑芥暟涓彲浠ヨ繘琛岃祫婧愭竻鐞嗗伐浣溿€俓n\n------\nwith璇彞涓嶄粎鍙互绠＄悊鏂囦欢锛岃繕鍙互绠＄悊閿併€佽繛鎺ョ瓑绛夛紝濡傦細\n```python\nimport  threading\nlock = threading.lock()\nwith lock:\n    pass\n```\n\n------\n\n### 涓婁笅鏂囩鐞嗗櫒\n涓婁笅鏂囩鐞嗗櫒鏄疄鐜颁簡涓婁笅鏂囧崗璁殑绫伙紝鑰屼笂涓嬫枃鍗忚灏辨槸涓€涓被瑕佸疄鐜癨\_\\_enter\\_\\_()鍜孿\_\\_exit\\_\\_()涓や釜鏂规硶銆備竴涓被鍙瀹炵幇浜哱\_\\_enter\\_\\_()鍜孿\_\\_exit\\_\\_()锛屽氨绉颁箣涓轰笂涓嬫枃绠＄悊鍣ㄣ€俓n\n- \\_\\_enter\\_\\_()锛氫富瑕佹墽琛屼竴浜涚幆澧冨噯澶囧伐浣滐紝鍚屾椂杩斿洖涓€璧勬簮瀵硅薄銆傚涓婁笅鏂囩鐞嗗櫒open(\"test.txt\")鐨刓\_\\_enter\\_\\_()鍑芥暟杩斿洖涓€涓枃浠跺璞°€俓n\n- \\_\\_exit\\_\\_()锛氬畬鏁村舰寮忎负`__exit__(type, value, traceback)`,杩欎笁涓弬鏁板拰璋冪敤sys.exec_info()鍑芥暟杩斿洖鍊兼槸涓€鏍风殑锛屽垎鍒负寮傚父绫诲瀷銆佸紓甯镐俊鎭拰鍫嗘爤銆傚鏋滄墽琛屼綋璇彞娌℃湁寮曞彂寮傚父锛屽垯杩欎笁涓弬鏁板潎琚涓篘one銆傚惁鍒欙紝瀹冧滑灏嗗寘鍚笂涓嬫枃鐨勫紓甯镐俊鎭€俓\_\\_exit\\_\\_()鏂规硶杩斿洖True鎴朏alse,鍒嗗埆鎸囩ず琚紩鍙戠殑寮傚父鏈夋病鏈夎澶勭悊銆傚鏋滆繑鍥濬alse锛屽紩鍙戠殑寮傚父灏嗕細琚紶閫掑嚭涓婁笅鏂囥€傚鏋淺\_\\_exit\\_\\_()鍑芥暟鍐呴儴寮曞彂浜嗗紓甯革紝鍒欎細瑕嗙洊鎵ц浣撶殑涓紩鍙戠殑寮傚父銆傚鐞嗗紓甯告椂锛屼笉闇€瑕侀噸鏂版姏鍑哄紓甯革紝鍙渶瑕佽繑鍥濬alse锛寃ith璇彞浼氭娴媆\_\\_exit\\_\\_()杩斿洖False鏉ュ鐞嗗紓甯搞€俓n\n銆€銆€濡傛灉瑕佽嚜瀹氫箟涓€涓笂涓嬫枃绠＄悊鍣紝鍙渶瑕佸畾涔変竴涓被骞朵笖瀹炵幇\\_\\_enter\\_\\_()鍜孿\_\\_exit\\_\\_()鍗冲彲銆備互鏁版嵁搴撶殑杩炴帴涓轰緥锛屽湪浣跨敤鏁版嵁搴撴椂锛屾湁鏃惰娑夊強鍒颁簨鍔℃搷浣溿€傛暟鎹簱鐨勪簨鍔℃搷浣滃綋璋冪敤commit()鎵цsql鍛戒护鏃讹紝濡傛灉鍦ㄨ繖涓繃绋嬩腑鎵ц澶辫触锛屽垯闇€瑕佹墽琛宺ollback()鍥炴粴鏁版嵁搴?閫氬父瀹炵幇鏂瑰紡鍙兘濡備笅锛歕n```python\ndef test():\n    con = MySQLdb.connection()\n    cursor = con.cursor()\n    sql = \"\"\"鍏蜂綋鐨剆ql璇彞\"\"\"\n    try:\n        cursor.execute(sql)\n        cursor.execute(sql)\n        cursor.execute(sql)\n        con.commit()      #鎻愪氦浜嬪姟\n    except Exception as e:\n        con.rollback()    #浜嬪姟鎵ц澶辫触锛屽洖婊氭暟鎹簱\n```\n濡傛灉鎯抽€氳繃with璇彞鏉ュ疄鐜版暟鎹簱鎵ц澶辫触鐨勫洖婊氭搷浣滐紝鍒欓渶瑕佽嚜瀹氫箟涓€涓暟鎹簱杩炴帴鐨勪笂涓嬫枃绠＄悊鍣紝鍋囪涓篋BConnection锛屽垯灏嗕笂闈㈢敤with璇彞鏉ュ疄鐜板涓嬶細\n\n```python\ndef test():\n    sql = \"\"\"鍏蜂綋鐨剆ql璇彞\"\"\"\n    con = DBConnection()\n    with con as cursor:   \n        cursor.execute(sql)\n        cursor.execute(sql)\n        cursor.execute(sql)\n```\nDBConnection鏁版嵁搴撲笂涓嬫枃绠＄悊鍣ㄥ垯闇€瑕佹彁渚涗竴涓嬪姛鑳斤細\\_\\_enter\\_\\_()瑕佽繑鍥炰竴涓繛鎺ョ殑cursor; 褰撴病鏈夊紓甯稿彂鐢熸椂锛孿\_\\_exit\\_\\_()鍑芥暟commit鎵€鏈夌殑鏁版嵁搴撴搷浣溿€傚鏋滄湁寮傚父鍙戠敓鍒橽\_\\_exit\\_\\_()浼氬洖婊氭暟鎹簱锛岃皟鐢╮ollback()銆傛墍浠ュ彲浠ュ疄鐜癉BConnection濡備笅锛歕n```python\nclass DBConnection():\n\n    def cursor(self):\n        #杩斿洖涓€涓父鏍囧苟涓斿惎鍔ㄤ竴涓簨鍔n        pass\n\n    def commit(self):\n        #鎻愪氦褰撳墠浜嬪姟\n        pass\n\n    def rollback(self):\n        #鍥炴粴褰撳墠浜嬪姟\n        pass\n\n    def __enter__(self):\n        #杩斿洖涓€涓猚ursor\n        cursor = self.cursor()\n        return cursor\n\n    def __exit__(self, type, value, traceback):\n        if traceback is None:\n            #娌℃湁寮傚父鍒欐彁浜や簨鍔n            self.commit()\n        else:\n            #鏈夊紓甯稿垯鍥炴粴鏁版嵁搴揬n            self.rollback()\n```\n\n### contextlib妯″潡\n鑷畾涔夊疄鐜癨\_\\_enter\\_\\_()鍜孿\_\\_exit\\_\\_()涓や釜鏂规硶鐨勭被,涓嶆槸寰堟柟渚裤€侾ython鐨刢ontextlib妯″潡鎻愪緵浜嗘洿鏂逛究鐨勬柟寮忔潵瀹炵幇涓€涓嚜瀹氫箟鐨勪笂涓嬫枃绠＄悊鍣ㄣ€俓ncontextlib妯″潡鍖呭惈涓€涓楗板櫒contextmanager鍜屼竴浜涜緟鍔╁嚱鏁帮紝瑁呴グ鍣╟ontextmanager鍙渶瑕佸啓涓€涓敓鎴愬櫒鍑芥暟灏卞彲浠ヤ唬鏇胯嚜瀹氫箟鐨勪笂涓嬫枃绠＄悊鍣紝鍏稿瀷鐢ㄦ硶锛歕n\n###### 閿佽祫婧愯嚜鍔ㄨ幏鍙栧拰閲婃斁鐨勪緥瀛? \n```python\n@contextmanager\ndef locked(lock):\n    lock.acquire()\n    try:\n        yield\n    finally:\n        lock.release()\n\nwith locked(myLock):\n    #浠ｇ爜鎵ц鍒拌繖閲屾椂锛宮yLock宸茬粡鑷姩涓婇攣\n    pass\n    #鎵ц瀹屽悗浼氾紝浼氳嚜鍔ㄩ噴鏀鹃攣\n```\n\n鐢熸垚鍣ㄥ嚱鏁扮殑鍘熺悊濡備笅锛歕n1. 鐢熸垚鍣ㄥ嚱鏁板湪鍦▂ield涔嬪墠鐨勪唬鐮佺瓑鍚屼簬涓婁笅鏂囩鐞嗗櫒涓殑\\_\\_enter\\_\\_鍑芥暟銆俓n2. yield鐨勮繑鍥炲€肩瓑鍚屼簬\\_\\_enter\\_\\_()鐨勮繑鍥炲€硷紝鍗冲鏋渨ith璇彞澹版槑浜哸s <variable>锛屽垯yield鐨勫€间細璧嬬粰variable\n3. 鐒跺悗鎵ц`finally`浠ｇ爜鍧楋紝绛夊悓浜庝笂涓嬫枃绠＄悊鍣ㄧ殑\\_\\_exit\\_\\_()銆傛鏃跺彂鐢熺殑浠讳綍寮傚父閮戒細鍐嶆閫氳繃yield杩斿洖銆俓n\n###### 鏂囦欢鎵撳紑鍚庤嚜鍔ㄧ鐞嗙殑瀹炵幇\n```python\n@contextmanager\ndef myopen(filename, mode=\"r\"):\n    f = open(filename,mode)\n    try:\n        yield f\n    finally:\n        f.close()\n\nwith myopen(\"test.txt\") as f:\n    for line in f:\n        print(line)\n```\n\n###### 鏁版嵁搴撲簨鍔″鐞哱n```python\n@contextmanager\ndef transaction(db):\n    db.begin()\n    try:\n        yield\n    except:\n        db.rollback()\n        raise\n    else:\n        db.commit()\n\nwith transaction(mydb):\n    mydb.cursor.execute(sql)\n    mydb.cursor.execute(sql)\n    mydb.cursor.execute(sql)\n```\n\n#### closing瀵硅薄\ncontextlib涓繕鍖呭惈涓€涓猚losing瀵硅薄锛岃繖涓璞″氨鏄竴涓笂涓嬫枃绠＄悊鍣紝瀹冪殑\\_\\_exit\\_\\_()浠呬粎璋冪敤浼犲叆鍙傛暟鐨刢lose鍑芥暟锛宑losing瀵硅薄鐨勬簮鐮佸涓嬶細\n```python\nclass closing(object):\n    def __init__(self, thing):\n        self.thing = thing\n    def __enter__(self):\n        return self.thing\n    def __exit__(self, *exc_info):\n        self.thing.close()\n```\n鎵€浠loseing涓婁笅鏂囩鐞嗗櫒浠呬娇鐢ㄤ簬鍏锋湁close()鏂规硶鐨勮祫婧愬璞°€備緥濡傦紝濡傛灉閫氳繃`urllib.request.urlopen`鎵撳紑涓€涓綉椤碉紝urlopen杩斿洖鐨剅equest鏈塩lose鏂规硶锛屾墍浠ュ氨鍙互浣跨敤closing涓婁笅鏂囩鐞嗗櫒锛歕n```python\nfrom urllib.request import urlopen\nfrom contextlib import closing\n\nwith closing(urlopen(\'https://www.baidu.com\')) as page:\n    for line in page:\n        print(line)\n```\n',1523928131.23953),('001523941317279f72c130fd32143ca8b6913952f98510c000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','鏁ｅ垪琛ㄦ煡鎵剧畻娉旵璇█瀹炵幇','from 澶ц瘽鏁版嵁缁撴瀯','```C\n#include <stdio.h>\n#include <stdlib.h>\n#define SUCCESS		1\n#define UNSUCCESS	0\n#define HASHSIZE	10      /* 鏁ｅ垪琛ㄩ暱搴?*/\n#define NULLKEY		-32768\ntypedef int Status;\ntypedef struct {\n	int	* arr;\n	int	cnt;            /* 褰撳墠鍏冪礌涓暟. 璨屼技鏍规湰娌＄敤鍒?*/\n}HashTable;                     /* 鍝堝笇琛?*/\n\n\nvoid init( HashTable* ph )\n{\n	/* HASHSIZE=HASHSIZE; */\n	ph->arr = (int *) malloc( HASHSIZE * sizeof(int) );\n	for ( int i = 0; i < HASHSIZE; ++i )\n	{\n		ph->arr[i] = NULLKEY;                   /* 鍒濆鍖栧叏涓篘ULLKEY */\n	}\n}\n\n\nint hash( int key )                                     /* 鏁ｅ垪鍑芥暟 */\n{\n	return(key % HASHSIZE);                         /* 闄ょ暀浣欐暟娉?*/\n}\n\n\nvoid insert( HashTable* ph, int key )\n{\n	int index = hash( key );                        /* 鏁ｅ垪鍦板潃 */\n	while ( ph->arr[index] != NULLKEY )             /* 涓嶄负绌哄垯鍐茬獊 */\n	{\n		index = (index + 1) % HASHSIZE;         /* 绾挎€ф帰娴嬪紑鏀惧湴鍧€娉?*/\n	}\n	ph->arr[index] = key;                           /* 鏈夌┖浣嶅垯鎻掑叆 */\n}\n\n\nStatus search( HashTable h, int key, int* index )\n{\n	*index = hash( key );                           /* 鏁ｅ垪鍦板潃 */\n	while ( h.arr[*index] != key )                  /* 濡傛灉涓嶇浉绛?鍒欏彲鑳藉瓨鍦ㄥ啿绐?*/\n	{\n		*index = (*index + 1) % HASHSIZE;       /* 绾挎€ф帰娴?*/\n		/* 濡傛灉閬囧埌绌轰綅鎴栧惊鐜簡涓€鍦堝垯娌℃壘鍒?*/\n		if ( h.arr[*index] == NULLKEY || *index == hash( key ) )\n		{\n			return(UNSUCCESS);\n		}\n	}\n	return(SUCCESS);\n}\n\n\nvoid print_arr( int* arr, int size )\n{\n	/* 鏍煎紡鍖栨墦鍗版暟缁?*/\n	printf( \"[\" );\n	for ( int i = 0; i < size - 1; ++i )\n	{\n		printf( \"%d, \", arr[i] );\n	}\n	printf( \"%d]\\n\", arr[size - 1] );\n}\n\n\nint main( int argc, char const *argv[] )\n{\n	/* int arr[]={12,67,56,16,25,37,22,29,15,47,48,34}; */\n	int		arr[] = { 40, 42, 96, 66, 13, 34, 98, 30, 67, 74 };\n	HashTable	ht;\n	init( &ht );\n	for ( int i = 0; i < HASHSIZE; ++i )\n	{\n		insert( &ht, arr[i] );\n	}\n	print_arr( ht.arr, HASHSIZE ); /* [40, 30, 42, 13, 34, 74, 96, 66, 98, 67] */\n\n	return(0);\n}\n\n```',1523941317.27939);
/*!40000 ALTER TABLE `blogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` varchar(50) NOT NULL,
  `blog_id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES ('0015233436390463994c342cd5941cabf49491bcad0418b000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','0015226508920485f05158265824f208a38ca1917420e32000','test4','http://www.gravatar.com/avatar/0e306c2e92417f462212dee62050e77f?d=mm&s=120','涓轰粈涔坢arkdown鏄繖涓笩鏍风殑锛?,1523343639.04609),('0015233502979373e2f07334a0b4f0ca9234a59ac2595e6000','00152325624799756f824c535de47e68d60b73a92eefbb1000','0015226508920485f05158265824f208a38ca1917420e32000','test4','http://www.gravatar.com/avatar/0e306c2e92417f462212dee62050e77f?d=mm&s=120','test',1523350297.93781),('0015234320087639705ab8f2bf74b849bcaef5dff216df5000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'http://www.gravatar.com/avatar/686338a44c5ada84f38551c44865fbea?d=mm&s=120','hello',1523432008.76358),('0015235193760612afd8d1a6f734bdf82d83d4a0f50a5e3000','0015234322193411ceb8f42260f4fd78dbc8d099f6bf672000','001523519358311d5701fc0fc4e4611a02d1966deec90a3000','test11','http://www.gravatar.com/avatar/bb26267f3c663a41ee85eaa1636f5766?s=40&d=identicon&r=g','hello',1523519376.06179),('001523519476028e374708b4ac24236896da45dc51d0ea8000','0015234322193411ceb8f42260f4fd78dbc8d099f6bf672000','001523519358311d5701fc0fc4e4611a02d1966deec90a3000','test11','http://www.gravatar.com/avatar/bb26267f3c663a41ee85eaa1636f5766?s=40&d=identicon&r=g','涓轰粈涔堟槸杩欎釜楦熸牱锛?,1523519476.02822),('00152351949628876ca6111cba145d98414d29bd6958b54000','0015234322193411ceb8f42260f4fd78dbc8d099f6bf672000','001523519358311d5701fc0fc4e4611a02d1966deec90a3000','test11','http://www.gravatar.com/avatar/bb26267f3c663a41ee85eaa1636f5766?s=40&d=identicon&r=g','<h1>hehe</h1>',1523519496.28888),('0015239336535076f892cbe92834fe09e982dd7f6ed3acf000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','## hello..',1523933653.50719),('001523933674691fd63ce7763af4c328eca5eae582db6f8000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','<h1>hello</h1>',1523933674.6912),('001523933685987ca4967c9bb624375be0d1db81a1469e9000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','111',1523933685.98718),('0015239336883483b27a5d21bbe44ffa15cf3b280bca068000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','222',1523933688.3488),('00152393369044752f38bdf69fb4c4a9d49bbbd4cf0204c000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','333',1523933690.44765),('001523933693752d80bdca6ad874669bef339d0352fcb65000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','444',1523933693.75261),('0015239336959287bd0139cbdd44e92a64f7f9612ded368000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','555',1523933695.92822),('001523933699936733b76b70a67460f94a8dd55c0b45c57000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','666',1523933699.93674),('0015239337050533847adc31f3841bf811e0d9ecd601522000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','777',1523933705.05342),('00152393371018310230fbe79684bd7a29a50281768f04c000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','888',1523933710.18337),('0015239337278205828faf7df024eccadb286ee57930abe000','001523324989288a806240e14b44bf4892a67e30f2ff7af000','00152325135242699631c079c264bd3a07dcd080c51732e000','hikari鏄?,'/static/img/456t.jpg','璨屼技璇勮娌℃湁鍒嗛〉鍟?..',1523933727.82018);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pwd` varchar(50) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(500) NOT NULL,
  `created_at` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('0015226482424214cf643dc9f3b4210ad51a3615eff2a04000','hikari@example.com','1234',0,'hikari','hikari.jpg',1522648242.37379),('001522648243243d46b968492a3445f9f591ad0fa519c1d000','maki@example.com','makimakima',0,'maki','about:blank',1522648243.24392),('00152264824333794a722bd4f514f739cba3be71eab2858000','rin@example.com','nyannyannyan',0,'rin','about:blank',1522648243.33774),('001522649384123c629360a46f4495390d76c509ae6f440000','nozomi@example.com','533b5d08080d5627f4871157fcd6ddd4124e1c9a',0,'nozomi','http://www.gravatar.com/avatar/a78533c9405151ff2d94442c958bb03a?d=mm&s=120',1522649384.23045),('00152264975323319b89590324d4684992660651eb93242000','abc@de.fg','d9f798a1c7a165a0d5e9ea33195882868ec8d2a7',0,'涓嶇煡閬?,'http://www.gravatar.com/avatar/7f632eff022a76bc39281afd411f0529?d=mm&s=120',1522649753.23333),('001522649913219bc9b71e90de34010a4646f8e289a9961000','test1@qq.com','e05cf96d2c8490b7a25dd48cf4065313f9847524',0,'test1','http://www.gravatar.com/avatar/ee9a0b354bfab5bebfc7f1d6fd7aac39?d=mm&s=120',1522649913.21981),('001522650064363fc77da7df324478587cb68351ec7e9fa000','test2@qq.com','8e13a0ff3af6554001d1463bd47f0553e83bbd39',0,'test2','http://www.gravatar.com/avatar/6ba9eaf83b8d35da49c4a18cbeb1c5c6?d=mm&s=120',1522650064.36363),('00152265065809545d2ac4b039b4ed7ba5243daa7d3f1d6000','test3@qq.com','31b9cd9ac0798553a2968418b7dee5b009203edd',0,'test3','http://www.gravatar.com/avatar/6789419e614a9588cade7d596dc4139a?d=mm&s=120',1522650658.09588),('0015226508920485f05158265824f208a38ca1917420e32000','test4@qq.com','8f34716bd116b23d1b14cfc878c75c3fdba63a47',0,'test4','http://www.gravatar.com/avatar/0e306c2e92417f462212dee62050e77f?d=mm&s=120',1522650892.04878),('001522654625942ce0e887d53e1483facf6d2c7e675fb2a000','test5@qq.com','f9ed82f0f56c6c257358ceae6beb3937ceb46757',0,'test5','http://www.gravatar.com/avatar/e2d609507e0a55cb3f5f66a3368d8c6d?d=mm&s=120',1522654625.94352),('001522656259957f33982bd6c6445c285e171210bb1f349000','hikari@qq.com','99d16de80859f2ee2950a6ad941ec60399c8c9b8',0,'hikari','http://www.gravatar.com/avatar/1b4ef0a8503d3130276f5093b8359964?d=mm&s=120',1522656259.95837),('001522657047369b13a683cf858464c9d8ad95e15029742000','kanan@lovelive.com','1f52d4bc9f195b4648eb2067dfa3d91980b62ff4',0,'matsuura_kanan','http://www.gravatar.com/avatar/43ebaa0d635b1355907122281b4f8508?d=mm&s=120',1522657047.37081),('001522660134529bd2993305bd440ea9cfe6a1eeea090ee000','test6@qq.com','e5aef6a1639cfed4e353d3f9e13e259074f7479d',0,'test6','http://www.gravatar.com/avatar/eb0c68c8bb17cdc5e79127778e56e6ad?d=mm&s=120',1522660134.53013),('001522660174261b367d07713a94bf49bd70e390b055cb3000','test7@qq.com','1e711220d6ff1060260f2ac0f598f969d733ad54',0,'test7','http://www.gravatar.com/avatar/9f2167efa17fd4b0cbce12882290a53d?d=mm&s=120',1522660174.2614),('001522660204356e733a0780d884012b038b00d8caa23d6000','test8@qq.com','4b000f5787d5b635c0df81f05ea9000ba0f74ef2',0,'test8','http://www.gravatar.com/avatar/4c9dee1b5bb729ec6411009d0f55b477?d=mm&s=120',1522660204.35636),('0015226602273876ac9f834f8bf472199891a36689f963e000','test9@qq.com','b77ceade6a312ee7e8a13bf0ba8fc0233ed25efc',0,'test9','http://www.gravatar.com/avatar/8ed06a4111533e65f89b7719881ab979?d=mm&s=120',1522660227.38722),('00152325135242699631c079c264bd3a07dcd080c51732e000','208343741@qq.com','b4396030dca4d1f7cdcd57237b02476dcba351ed',1,'hikari鏄?,'/static/img/456t.jpg',1523251352.52433),('0015235193091912573403780774edf8a586689c242f36c000','test10@qq.com','af6aa288710d9e31c6024f71920920ce40073d68',0,'test10','http://www.gravatar.com/avatar/f3c95339bfd9c60dd274964035d22568?d=mm&s=120',1523519309.23145),('001523519358311d5701fc0fc4e4611a02d1966deec90a3000','test11@qq.com','8be7a53c9cedc379fc26cc1bc328e0ac3d6848e0',0,'test11','http://www.gravatar.com/avatar/bb26267f3c663a41ee85eaa1636f5766?s=40&d=identicon&r=g',1523519358.3115),('00152351962374944c3a742f8ed4b3996f068f62833694f000','hoshizora_rin@gmail.com','2d7c77a221bdfb2f797fff40a75668bd8c6ae699',0,'鏄熺┖鍑?,'http://www.gravatar.com/avatar/33a5c7e21690a21fc2172147285c2648?s=80&d=identicon&r=g',1523519623.74989);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-17 13:42:09
