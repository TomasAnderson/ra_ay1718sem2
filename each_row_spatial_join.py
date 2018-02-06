__author__ = 'lww'

# coding=utf-8
import arcpy,os,codecs
# arcpy.env.workspace="E:\\"
# fc="user_active_live.dbf"
# rows=arcpy.SearchCursor(fc)
#
# i=0
# for r in rows:
#     id=r.getValue("uid")
#     print(id)
def creat_xy_point(x,y,filef):
    rows=arcpy.InsertCursor(filef)
    row = rows.newRow()
    point.X=x
    point.Y=y
    pointGeometry=arcpy.PointGeometry(point)
    #pointGeometryList.append(pointGeometry)
    row.shape=pointGeometry
    rows.insertRow(row)
    del  row
    del rows

def clear_lyr(filef):
    rows=arcpy.UpdateCursor(filef)
    for row in rows:
        rows.deleteRow(row)
        del  row
    del rows

def get_value(filef,field_name):
    rows=arcpy.SearchCursor(filef)
    for row in rows:
        b=row.getValue(field_name)
        return b
        del  row
    del rows
f_in=codecs.open("E:\\temp\users_active_live.csv", "r")
f_out=codecs.open("E:\\temp\users_active_livejoin_300.csv", "w", encoding = "utf-8")
join_features = "E:\\temp\\new_fishnet_300.shp"
#现在test.gdb里建一个空的POINT文件，命名为point,不需要建立point_join这个文件
f_temp="E:\\temp\\test.gdb\\point"
f_temp_out="E:\\temp\\test.gdb\\point_join"
point=arcpy.Point()
a=0
b=0
uid_pot=[]
clear_lyr(f_temp)
rows1=arcpy.InsertCursor(f_temp)

batch_num=10000

for f in f_in:
    a=a+1
    print(a)
    if a==1:
        continue
    b=b+1
    if b<=batch_num:
	#这里是你的表头
        [uid,long,lat,uid2,long_live,lat_live]=f.strip().split(',')
        uid_pot.append(uid)
        uid_pot.append(uid2)
        row = rows1.newRow()
        point.X=long
        point.Y=lat
        pointGeometry=arcpy.PointGeometry(point)
        #pointGeometryList.append(pointGeometry)
        row.shape=pointGeometry
        rows1.insertRow(row)
        #del  row
        #row = rows1.newRow()
        point.X=long_live
        point.Y=lat_live
        pointGeometry=arcpy.PointGeometry(point)
        #pointGeometryList.append(pointGeometry)
        row.shape=pointGeometry
        rows1.insertRow(row)
        del  row
        #
        # creat_xy_point(long,lat,f_temp)
        # creat_xy_point(long_live,lat_live,f_temp)
    else:
        del rows1
        b=0
        arcpy.SpatialJoin_analysis(f_temp, join_features, f_temp_out)
        rows=arcpy.SearchCursor(f_temp_out)
        k=-1
        for row in rows:
            k=k+1
            active_point_id=row.getValue("Id")
            uid=uid_pot[k]
            row=rows.next()
            k=k+1
            #print k
            live_point_id=row.getValue("Id")
            if active_point_id!=None and live_point_id!=None and active_point_id!=live_point_id :
                strwrite=uid+","+str(active_point_id)+","+str(live_point_id)+"\n"
                f_out.write(strwrite)

        #del row
        del rows
        clear_lyr(f_temp)
        arcpy.Delete_management(f_temp_out)
        rows1=arcpy.InsertCursor(f_temp)
        uid_pot=[]

f_out.close()
f_in.close()

