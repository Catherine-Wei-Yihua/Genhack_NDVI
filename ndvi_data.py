import rasterio
import numpy as np

def tif_info(file_path):
    with rasterio.open(file_path) as src:
        print("=== TIFF FILE INFORMATION ===")
        print(f"File: {file_path}")
        print(f"Driver: {src.driver}")
        print(f"Number of Bands: {src.count}")
        print(f"Width: {src.width} pixels")
        print(f"Height: {src.height} pixels")
        print(f"Data Type: {src.dtypes[0]}")
        print(f"CRS: {src.crs}")
        print(f"Transform: {src.transform}")
        print(f"Bounds: {src.bounds}")
        print(f"NoData Value: {src.nodata}")
        
        # Band-specific information
        for i in range(1, src.count + 1):
            band = src.read(i)
            print(f"\n--- Band {i} ---")
            print(f"  Min: {np.nanmin(band)}")
            print(f"  Max: {np.nanmax(band)}")
            print(f"  Mean: {np.nanmean(band)}")
            print(f"  Std: {np.nanstd(band)}")
            print(f"  Shape: {band.shape}")

# Usage
tif_info("/Users/yihua/Desktop/花花Catherine/大学（UCSB）/活动相关/UCSB DS/Genhack/Data/sentinel_ndvi/ndvi_2023-09-01_2023-12-01.tif")