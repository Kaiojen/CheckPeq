# 🔧 Guia de Resolução de Problemas

## Problemas Comuns e Soluções

### 1. Sistema não inicia / Tela fica carregando para sempre

**Sintomas:**

- Streamlit fica em "Please wait..."
- Sistema não carrega a interface

**Soluções:**

1. Execute `CORRIGIR_RAPIDO.bat`
2. Execute `TESTAR_SISTEMA.bat` para diagnóstico
3. Verifique se todos os diretórios existem:
   - database/
   - reports/
   - uploads/
   - temp/

### 2. Erro "No module named streamlit"

**Solução:**

```batch
# Execute na ordem:
1. INSTALAR.bat
2. CORRIGIR_RAPIDO.bat
3. EXECUTAR.bat
```

### 3. Sistema não lê arquivos PDF/DOCX

**Possíveis causas:**

- Google API não configurada
- Arquivo corrompido
- Arquivo muito grande (>16MB)

**Soluções:**

1. Configure a API: `CONFIGURAR_API.bat`
2. Teste com arquivo menor
3. Use `TESTAR_SIMPLES.bat` para verificar

### 4. Erro ao importar módulos de segurança

**Solução:**
O sistema funciona sem os módulos de segurança. Os avisos podem ser ignorados.

### 5. "GOOGLE_API_KEY não configurada"

**Solução:**

1. Execute `CONFIGURAR_API.bat`
2. Ou crie arquivo `.env` com:

```
GOOGLE_API_KEY=sua_chave_aqui
```

## Scripts de Diagnóstico

### Para teste rápido:

```batch
TESTAR_SIMPLES.bat
```

### Para diagnóstico completo:

```batch
DIAGNOSTICO.bat
```

### Para teste detalhado:

```batch
TESTAR_SISTEMA.bat
```

## Reinstalação Limpa

Se nada funcionar:

1. Delete a pasta `venv`
2. Execute `INSTALAR.bat`
3. Execute `CORRIGIR_RAPIDO.bat`
4. Configure a API
5. Execute o sistema

## Suporte

Se o problema persistir após todas as tentativas:

1. Execute `TESTAR_SISTEMA.bat`
2. Salve o resultado
3. Verifique os logs em `logs/`
