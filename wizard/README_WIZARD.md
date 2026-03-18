# Wizard de Impressão do Laudo de Liberação

## Descrição

O Wizard de Impressão permite selecionar quais materiais serão incluídos no Laudo de Liberação de Produtos. Isso é especialmente útil quando um ciclo contém diversos materiais, mas você deseja gerar laudos específicos para diferentes clientes ou situações.

## Como Usar

### 1. Acessar o Wizard

Existem três formas de abrir o wizard:

**Opção A: Pelo Botão no Header do Formulário (Recomendado)**
1. Abra o formulário de um ciclo de esterilização
2. Clique no botão destacado **"Gerar Laudo de Liberação"** no header (próximo aos botões de ação)
   - 💡 Este botão só aparece se o ciclo tiver materiais cadastrados
   - 🎨 Botão destacado em cor primária

**Opção B: Pelo Menu Imprimir**
1. No formulário do ciclo, clique em "Imprimir"
2. Selecione "Laudo de Liberação de Produtos"
3. O wizard abre automaticamente

**Opção C: Pelo Menu de Ação**
1. No formulário do ciclo, clique em "Ação"
2. Selecione "Laudo de Liberação de Produtos"
3. O wizard abre automaticamente

### 2. Interface do Wizard

O wizard exibe:

**Cabeçalho:**
- Nome do ciclo
- Título: "Laudo de Liberação de Produtos"

**Informações:**
- **Materiais Selecionados**: Contador em tempo real mostrando quantos materiais foram marcados

**Tabela de Materiais:**
Lista todos os materiais do ciclo com as colunas:
- Descrição do Material
- Fabricante
- Lote
- Quantidade
- Unidade
- Validade

**Botões de Ação:**
- 🖨️ **Gerar Laudo**: Imprime o laudo com os materiais selecionados
- ❌ **Cancelar**: Fecha o wizard

### 3. Selecionar Materiais

**Seleção Individual:**
- Clique na checkbox ao lado de cada material para marcá-lo/desmarcá-lo
- Por padrão, **nenhum material vem selecionado** - você deve marcar manualmente

**Nenhum Atalho de Seleção em Massa:**
- Não há botões de atalho - você deve marcar cada material individualmente
- Isso garante que você selecione conscientemente cada item do laudo

**Contador de Seleção:**
- O número de materiais selecionados é exibido em tempo real
- Ajuda a controlar quantos itens serão incluídos no laudo

### 4. Gerar o Laudo

1. Selecione os materiais desejados
2. Clique em **"Gerar Laudo"**
3. O PDF será gerado contendo apenas os materiais selecionados

⚠️ **Importante:** É necessário selecionar pelo menos um material. O botão "Gerar Laudo" fica desabilitado até que você selecione algum material.

## Recursos do Wizard

### ✅ Comportamento Padrão

Ao abrir o wizard:
- **Nenhum material vem selecionado** por padrão
- Você deve marcar manualmente cada material desejado usando as checkboxes
- Não há atalhos - seleção totalmente manual

### 🔄 Comportamento Dinâmico

- **Contador automático**: Atualiza em tempo real conforme você seleciona/desmarca
- **Validação**: Não permite gerar laudo sem materiais selecionados
- **Feedback visual**: Materiais selecionados aparecem destacados em verde

### 📋 Integração com o Laudo

Os materiais selecionados no wizard:
- Aparecem na tabela "PRODUTOS ESTERILIZADOS" do laudo
- São numerados sequencialmente (1, 2, 3...)
- Mantêm todas as informações (lote, validade, etc.)

## Casos de Uso

### Caso 1: Laudo Completo
**Situação:** Gerar laudo com todos os materiais do ciclo

**Passos:**
1. Abra o wizard
2. **Marque todos os materiais** um por um nas checkboxes
3. Clique em "Gerar Laudo"

### Caso 2: Laudo Parcial para Cliente Específico
**Situação:** Cliente X comprou apenas alguns itens do ciclo

**Passos:**
1. Abra o wizard
2. Marque apenas os materiais do Cliente X (checkboxes individuais)
3. Clique em "Gerar Laudo"

### Caso 3: Múltiplos Laudos do Mesmo Ciclo
**Situação:** Gerar laudos separados para diferentes clientes

**Passos:**
1. Gere o primeiro laudo com materiais do Cliente A
2. Abra o wizard novamente
3. Selecione materiais do Cliente B
4. Gere o segundo laudo
5. Repita para outros clientes

### Caso 4: Laudos por Tipo de Material
**Situação:** Separar materiais por categoria ou tipo

**Passos:**
1. Abra o wizard
2. Marque apenas materiais de uma categoria (ex: instrumentos)
3. Gere o laudo
4. Abra o wizard novamente
5. Marque materiais de outra categoria
6. Gere outro laudo

## Validações e Avisos

### ⚠️ Nenhum Material Selecionado
- **Mensagem**: "Selecione pelo menos um material para gerar o laudo"
- **Ação**: O botão "Gerar Laudo" fica invisível/desabilitado
- **Solução**: Selecione pelo menos um material

### ℹ️ Instruções no Wizard
O wizard exibe uma caixa de informações:
> "**Instruções:** Selecione os materiais que deseja incluir no laudo de liberação. Somente os materiais marcados aparecerão no documento final."

## Acesso ao Wizard

### 🎯 Todas as Formas de Acesso Abrem o Wizard

**Não há mais impressão direta!** Todas as opções de acesso ao laudo agora abrem o wizard para seleção de materiais:

1. **Botão no Header**: "Gerar Laudo de Liberação" (destacado)
2. **Menu Imprimir**: "Laudo de Liberação de Produtos"
3. **Menu Ação**: "Laudo de Liberação de Produtos"
4. **Botão Estatístico**: Botão "Materiais" no formulário (opcional)

Todas essas opções levam ao wizard onde você pode:
- ✅ Selecionar todos os materiais (padrão)
- ✅ Selecionar materiais específicos
- ✅ Gerar laudo personalizado

## Dicas e Boas Práticas

### ✅ Recomendações

1. **Revise a seleção** antes de gerar o laudo
2. **Use nomes descritivos** nos materiais para facilitar identificação
3. **Gere laudos separados** para diferentes clientes
4. **Mantenha rastreabilidade** salvando os PDFs gerados

### 💡 Dicas de Uso

- **Seleção consciente**: Marque apenas o que realmente precisa no laudo
- **Sem atalhos**: Cada material deve ser marcado individualmente
- **Múltiplos laudos**: O wizard pode ser aberto várias vezes para o mesmo ciclo
- **Ordem**: Materiais aparecem no laudo na mesma ordem da tabela

### ⚡ Produtividade

- Para qualquer laudo: marque os materiais necessários → "Gerar Laudo"
- Para gerar vários laudos rapidamente: mantenha o formulário do ciclo aberto
- Organize os materiais na tabela antes para facilitar a seleção

## Estrutura Técnica

### Model: `wizard.print.laudo`

**Campos:**
- `ciclo_id`: Referência ao ciclo
- `material_line_ids`: Many2many com materiais selecionados
- `select_all`: Boolean para marcar/desmarcar todos
- `material_count`: Contador computed de materiais

**Métodos:**
- `action_print_laudo()`: Gera o laudo com materiais selecionados
- `action_select_all_materials()`: Seleciona todos os materiais
- `action_deselect_all_materials()`: Remove todas as seleções

### Arquivos

- **Model**: `wizard/wizard_print_laudo.py`
- **View**: `wizard/wizard_print_laudo_views.xml`
- **Security**: `security/ir.model.access.csv`

## Solução de Problemas

### Problema: Botão "Gerar Laudo" não aparece
**Causa**: O ciclo não tem materiais cadastrados
**Solução**: Adicione materiais na aba "Materiais Esterilizados" do ciclo

### Problema: Wizard abre vazio
**Causa**: Contexto do ciclo não foi passado
**Solução**: Sempre abra o wizard a partir do formulário do ciclo

### Problema: Materiais não aparecem no laudo
**Causa**: Nenhum material foi selecionado ou validação falhou
**Solução**: Verifique se os materiais estão marcados antes de gerar

## Suporte

Para dúvidas ou sugestões sobre o wizard:
- **AFR Sistemas**
- Website: https://www.afrsistemas.com.br

