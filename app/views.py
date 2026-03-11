from django.shortcuts import render, redirect
import easyocr
import os
from django.conf import settings

def index(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # 保存上传的文件到static/uploads目录
        image = request.FILES['image']
        # 处理STATIC_ROOT为None的情况
        if settings.STATIC_ROOT:
            upload_dir = os.path.join(settings.STATIC_ROOT, 'uploads')
        else:
            # 使用BASE_DIR作为默认值
            upload_dir = os.path.join(settings.BASE_DIR, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        image_path = os.path.join(upload_dir, image.name)
        
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        
        # 生成图片URL
        image_url = f'/static/uploads/{image.name}'
        
        # 使用easyocr进行日文文本识别
        reader = easyocr.Reader(['ja'])
        try:
            results = reader.readtext(image_path)
            result = ' '.join([text for _, text, _ in results])
        except Exception as e:
            result = f'识别失败: {str(e)}'
        
        # 跳转到结果页面
        from django.urls import reverse
        return redirect(f"{reverse('result')}?result={result}&image_url={image_url}")
    
    return render(request, 'index.html')

def result(request):
    # 从URL参数获取结果和图片URL
    result = request.GET.get('result', '')
    image_url = request.GET.get('image_url', '')
    
    return render(request, 'result.html', {'result': result, 'image_url': image_url})
