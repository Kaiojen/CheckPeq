@echo off
echo ================================================================
echo          CORRIGINDO ERRO DO RAILWAY
echo ================================================================
echo.

echo [1] Versoes atualizadas:
echo    - streamlit: 1.46.1 -^> 1.32.2 (versao mais estavel)
echo    - pandas: 2.3.0 -^> 2.0.3 (compatibilidade)
echo    - numpy: 2.3.1 -^> 1.24.3 (compatibilidade)
echo.

echo [2] Fazendo commit das correcoes...
git add requirements.txt
git commit -m "Fix: Atualizar versoes das dependencias para compatibilidade Railway"

echo.
echo [3] Enviando para o GitHub...
git push

echo.
echo ================================================================
echo              PRONTO! 
echo ================================================================
echo.
echo O Railway deve detectar as mudancas automaticamente e tentar
echo fazer o deploy novamente.
echo.
echo Se nao funcionar automaticamente:
echo 1. Va para o Railway
echo 2. Clique em "Redeploy"
echo.
pause 