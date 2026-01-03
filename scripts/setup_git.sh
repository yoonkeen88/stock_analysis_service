#!/bin/bash

# GitHub 저장소 초기화 스크립트

echo "🚀 GitHub 저장소 초기화를 시작합니다..."

# Git 초기화
if [ ! -d ".git" ]; then
    echo "📦 Git 저장소 초기화 중..."
    git init
    echo "✅ Git 저장소가 초기화되었습니다."
else
    echo "⚠️  Git 저장소가 이미 초기화되어 있습니다."
fi

# .gitignore 확인
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore 파일이 존재합니다."
else
    echo "⚠️  .gitignore 파일이 없습니다."
fi

# 첫 커밋
echo ""
echo "📝 첫 커밋을 준비합니다..."
git add .
git commit -m "Initial commit: Stock Analysis Service

- FastAPI 백엔드 구조 설정
- React 프론트엔드 기본 구조
- 데이터베이스 모델 (StockData, Prediction, PredictionLog, NewsLog, PaperInsight)
- API 엔드포인트 (stocks, predictions, news, evaluation, dashboard)
- 스키마 다이어그램 자동 생성 스크립트"

echo ""
echo "✅ 첫 커밋이 완료되었습니다!"
echo ""
echo "📋 다음 단계:"
echo "1. GitHub에서 새 저장소를 생성하세요: https://github.com/new"
echo "2. 아래 명령어로 원격 저장소를 추가하고 푸시하세요:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/stock_analysis_service.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

