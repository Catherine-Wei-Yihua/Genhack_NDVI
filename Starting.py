import rasterio

# 打开文件
with rasterio.open("/Users/yihua/Downloads/2020_10m_u_component_of_wind_daily_mean.nc") as src:
    ndvi = src.read(1)   # 读第一波段
    profile = src.profile   # 元数据（坐标、分辨率等）

print(ndvi.shape)
print(profile)
