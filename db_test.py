import pylmdb as lmdb
import numpy as np
if __name__ == '__main__':
    # 创建数据
    X = np.random.random((8, 2, 2, 2, 2))
    y = np.arange(2, dtype=np.uint8)

    # 创建
    db =  lmdb.Writer(dirpath=r'data', map_size_limit=1)
    print(db)
    db.put_samples({'input1': X, 'target1': y})
    db.put_samples({"jaw":np.array("upper"),"name":np.array("数据5aaaaaaaaaaa")})
    db.set_meta_str("第一个描述信息", "这是创建")
    db.close()



    # 追加并扩容
    db = lmdb.Writer(dirpath=r'data', map_size_limit=50)
    print(db)
    for i in range(100):
        db.put_samples({'rangeX': X, 'rangeY':X})
    db.set_meta_str("第二个描述信息", "追加")
    db.close()



    #修改,将索引为2的修改为新的内容
    db = lmdb.Writer(dirpath=r'data', map_size_limit=10)
    db.change_db_value(2,{'y':y, 'x':y})
    db.close()


    # 修复windows无法实时变化大小
    lmdb.repair_windows_size(dirpath=r'data')





    # 读取
    db = lmdb.Reader(dirpath=r'data')
    print(db)
    print(db.get_meta_key_info())
    print(db.get_data_key_info())
    print(db.get_meta_str("第一个描述信息"))
    print(db.get_meta_str("第二个描述信息"))
    print(db[2].keys())
    print(db[1].keys())
    print(db[0].keys())
    db.close()



    # 合并数据库
    db_A =  lmdb.Writer(dirpath=r'A', map_size_limit=1)
    db_A.put_samples({'inputA': X, 'targetA': y})
    db_A.set_meta_str("第一个描述信息", "这是A")
    db_A.close()

    db_B=  lmdb.Writer(dirpath=r'B', map_size_limit=1)
    db_B.put_samples({'inputB': X, 'targetB': y})
    db_B.set_meta_str("第二个描述信息", "这是B")
    db_B.close()

    lmdb.merge_db(merge_dirpath=r'C', A_dirpath="A", B_dirpath="B",map_size_limit=2)
    # 读取
    db = lmdb.Reader(dirpath=r'C')
    print(db)
    print(db.get_meta_key_info())
    print(db.get_data_key_info())
    print(db.get_meta_str("第一个描述信息"))
    print(db.get_meta_str("第二个描述信息"))
    print(db[1].keys())
    print(db[0].keys())
    #print(db[0])
    db.close()

