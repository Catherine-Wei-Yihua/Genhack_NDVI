import rasterio
import numpy as np
from rasterio.windows import Window
import math

file_path = "/Users/yihua/Desktop/花花Catherine/大学（UCSB）/活动相关/UCSB DS/Genhack/Data/sentinel_ndvi/ndvi_2023-09-01_2023-12-01.tif"

def calculate_large_raster_stats(file_path, sample_fraction=0.01):
    """Calculate statistics for very large rasters using sampling"""
    
    with rasterio.open(file_path) as src:
        print("=== ORIGINAL DATA ===")
        print(f"Shape: {src.height} x {src.width} = {src.height * src.width:,} pixels")
        print(f"Data type: {src.dtypes[0]}")
        print(f"NoData value: {src.nodata}")
        
        # METHOD 1: Sample-based statistics (recommended for huge files)
        print(f"\n=== CALCULATING STATISTICS (sampling {sample_fraction*100}% of data) ===")
        
        # Calculate sample size
        total_pixels = src.height * src.width
        sample_size = int(total_pixels * sample_fraction)
        window_size = 1000  # Process in 1000x1000 pixel windows
        
        stats = {
            'count': 0,
            'sum': 0.0,
            'sum_squares': 0.0,
            'min': float('inf'),
            'max': float('-inf'),
            'values': []
        }
        
        # Sample random windows throughout the image
        for i in range(int(sample_size / (window_size * window_size)) + 1):
            # Random window position
            row = np.random.randint(0, max(1, src.height - window_size))
            col = np.random.randint(0, max(1, src.width - window_size))
            
            try:
                window = Window(col, row, 
                              min(window_size, src.width - col), 
                              min(window_size, src.height - row))
                
                data = src.read(1, window=window)
                
                # Process the window
                valid_mask = data != 255
                if np.any(valid_mask):
                    valid_data = data[valid_mask]
                    # Rescale to NDVI
                    ndvi_data = (valid_data.astype(np.float32) / 127.0) - 1.0
                    
                    # Update statistics
                    stats['count'] += len(ndvi_data)
                    stats['sum'] += np.sum(ndvi_data)
                    stats['sum_squares'] += np.sum(ndvi_data ** 2)
                    stats['min'] = min(stats['min'], np.min(ndvi_data))
                    stats['max'] = max(stats['max'], np.max(ndvi_data))
                    
                    # Sample some values for distribution
                    if len(ndvi_data) > 1000:
                        stats['values'].extend(np.random.choice(ndvi_data, 1000, replace=False).tolist())
                    else:
                        stats['values'].extend(ndvi_data.tolist())
                        
            except Exception as e:
                continue
        
        if stats['count'] > 0:
            mean = stats['sum'] / stats['count']
            std = math.sqrt((stats['sum_squares'] / stats['count']) - (mean ** 2))
            
            print(f"Sample size: {stats['count']:,} pixels")
            print(f"Min NDVI: {stats['min']:.3f}")
            print(f"Max NDVI: {stats['max']:.3f}")
            print(f"Mean NDVI: {mean:.3f}")
            print(f"Std NDVI: {std:.3f}")
            
            # Calculate distribution from sampled values
            if stats['values']:
                values_array = np.array(stats['values'])
                print(f"\n=== NDVI DISTRIBUTION (from {len(values_array):,} samples) ===")
                
                bins = [-1.0, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]
                categories = ['Water', 'Barren', 'Sparse Veg', 'Moderate Veg', 'Healthy Veg', 'Dense Veg', 'Very Dense Veg']
                
                counts, bin_edges = np.histogram(values_array, bins=bins)
                
                for i, (category, count) in enumerate(zip(categories, counts)):
                    percentage = (count / len(values_array)) * 100
                    print(f"{category:15}: {count:>8,} samples ({percentage:5.1f}%)")
        
        # METHOD 2: Quick overview of first few rows (alternative approach)
        print(f"\n=== QUICK OVERVIEW (first 1000x1000 pixels) ===")
        data_sample = src.read(1, window=Window(0, 0, 1000, 1000))
        valid_mask = data_sample != 255
        valid_count = np.sum(valid_mask)
        
        if valid_count > 0:
            valid_data = data_sample[valid_mask]
            ndvi_sample = (valid_data.astype(np.float32) / 127.0) - 1.0
            
            print(f"Sample area: {valid_count:,} valid pixels")
            print(f"Min NDVI: {np.min(ndvi_sample):.3f}")
            print(f"Max NDVI: {np.max(ndvi_sample):.3f}")
            print(f"Mean NDVI: {np.mean(ndvi_sample):.3f}")

# Run the analysis
calculate_large_raster_stats(file_path)