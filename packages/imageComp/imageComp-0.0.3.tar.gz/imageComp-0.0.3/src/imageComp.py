from PIL import Image
import numpy as np
from sklearn.decomposition import PCA

def compress_image(image, n_components):
    # 画像をグレースケールに変換
    image = image.convert('L')
    image_data = np.array(image)
    
    # 主成分分析を実行
    pca = PCA(n_components=n_components)
    pca.fit(image_data)
    
    # 圧縮された画像データを取得
    compressed_image_data = pca.transform(image_data)
    
    # 圧縮された画像データを元の形状に戻す
    reconstructed_image_data = pca.inverse_transform(compressed_image_data)
    
    # 画像データの型を整数型に変換
    reconstructed_image_data = reconstructed_image_data.astype(np.uint8)
    
    # 圧縮された画像を作成
    compressed_image = Image.fromarray(reconstructed_image_data)

    save_image = compressed_image.save('compressed_image.jpg')

    return save_image
    

def main():
    img = input("Enter the path to the image:")
    img = Image.open(img)
    n_components = 100
    compress_image(img, n_components)

if __name__ == "__main__":
    main()