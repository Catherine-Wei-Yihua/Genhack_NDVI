import rasterio
import matplotlib.pyplot as plt

# 1. 打开 tif
tif_path = r"/Users/yihua/Desktop/花花Catherine/大学（UCSB）/活动相关/UCSB DS/Genhack/Data/sentinel_ndvi/ndvi_2020-03-01_2020-06-01.tif"
with rasterio.open("/Users/yihua/Desktop/花花Catherine/大学（UCSB）/活动相关/UCSB DS/Genhack/Data/sentinel_ndvi/ndvi_2020-03-01_2020-06-01.tif"
) as src:
    arr = src.read(1)   # 第一波段
    profile = src.profile
    print("CRS:", src.crs)
    print("Transform:", src.transform)
    print("Shape:", arr.shape)
    
#plt.imshow(arr, cmap="RdYlGn")
#plt.colorbar(label='NDVI')
#plt.title("NDVI")
#plt.show()


