from geodeticengine import CoordTrans

print("Engineering")
points = [[8911.832,5139.165]]
crs_from = "EQUINOR:4100002"
trans_from = "EQUINOR:3100002"
crs_to = "EPSG:25832"
ct = CoordTrans(crs_from=crs_from, crs_to=crs_to, trans_from=trans_from, points=points)
print(f"from:{ct.transform_pointlist()}")
points_to=[[283341.96397220856,6748519.897517173]]
ct = CoordTrans(crs_from=crs_to, crs_to=crs_from, trans_to=trans_from, points=points_to)
print(f"from:{ct.transform_pointlist()}")
