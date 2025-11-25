import rasterio

file_path = "/Users/yihua/Desktop/花花Catherine/大学（UCSB）/活动相关/UCSB DS/Genhack/Data/sentinel_ndvi/ndvi_2019-12-01_2020-03-01.tif"

with rasterio.open(file_path) as src:
    print("Driver:", src.driver)
    print("CRS:", src.crs)
    print("Transform:", src.transform)
    print("Shape (height, width):", src.height, src.width)
    print("Number of bands:", src.count)
    print("\nMetadata keys:")
    print(src.meta)

    # Print all tags stored in file
    print("\nAll tags (metadata in the TIFF):")
    print(src.tags())

    # Print tags for each band
    for i in range(1, src.count+1):
        print(f"\nBand {i} tags:")
        print(src.tags(i))
