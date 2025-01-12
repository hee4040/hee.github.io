import torch
import sys
from pathlib import Path

# YOLOv5 코드 경로 추가 (본인의 YOLOv5 경로로 수정하세요)
sys.path.append(r"C:\Users\zerom\Desktop\숭실\프밍실2\yolov5")

# 가중치 파일 경로
old_weights_path = r"C:\Users\zerom\Desktop\숭실\프밍실2\코드\best.pt"
new_weights_path = r"C:\Users\zerom\Desktop\숭실\프밍실2\코드\best_fixed.pt"

try:
    print(f"기존 가중치를 '{old_weights_path}'에서 로드 중...")
    checkpoint = torch.load(old_weights_path, map_location="cpu")
    torch.save(checkpoint, new_weights_path)
    print(f"새로운 가중치를 '{new_weights_path}'에 저장 완료.")
except Exception as e:
    print(f"가중치 변환 중 오류 발생: {e}")
