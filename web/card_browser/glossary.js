// 五行卡牌术语悬浮高亮插件
(function() {
  let state = {
    initialized: false,
    terms: [], // list of term objects: {word: "普通学会", term: {...}}
    tooltipBox: null
  };

  // 动态注入样式
  function injectStyles() {
    const css = `
      .glossary-term {
        border-bottom: 1px dashed var(--accent, #256b5f);
        color: var(--accent, #256b5f);
        cursor: help;
        font-weight: bold;
        display: inline;
      }
      .glossary-term:hover {
        background-color: rgba(37, 107, 95, 0.1);
      }
      .glossary-tooltip-box {
        position: absolute;
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        padding: 12px;
        border-radius: 6px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
        font-size: 13px;
        line-height: 1.5;
        width: 300px;
        z-index: 99999;
        pointer-events: none;
        display: none;
        text-align: left;
      }
      .glossary-tooltip-header {
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 6px;
        font-size: 14px;
        border-bottom: 1px solid #334155;
        padding-bottom: 4px;
      }
      .glossary-tooltip-category {
        font-size: 10px;
        color: #94a3b8;
        float: right;
        font-weight: normal;
        margin-top: 2px;
      }
      .glossary-tooltip-body {
        color: #e2e8f0;
      }
      .glossary-tooltip-examples {
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px dashed #334155;
        font-size: 11px;
        color: #94a3b8;
        font-style: italic;
      }
    `;
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  // 初始化获取术语定义
  async function init() {
    if (state.initialized) return;
    injectStyles();

    // 创建悬浮框 DOM 并加入 body
    const box = document.createElement('div');
    box.className = 'glossary-tooltip-box';
    document.body.appendChild(box);
    state.tooltipBox = box;

    try {
      const res = await fetch('/api/glossary');
      if (!res.ok) throw new Error('获取术语库失败');
      const data = await res.json();
      
      const rawTerms = data.terms || [];
      const termsList = [];

      // 提取每个 term 及其别名，并按字符长度倒序排列（先匹配长句如“完美学会”，再匹配短句如“学会”）
      rawTerms.forEach(t => {
        if (t.status === 'deprecated') return; // 跳过废弃术语
        
        // 词库自身
        termsList.push({
          word: t.term,
          term: t
        });

        // 别名
        if (t.aliases && Array.isArray(t.aliases)) {
          t.aliases.forEach(alias => {
            if (alias && alias.trim()) {
              termsList.push({
                word: alias.trim(),
                term: t
              });
            }
          });
        }
      });

      // 排序：长度长的排前面
      termsList.sort((a, b) => b.word.length - a.word.length);
      state.terms = termsList;
      state.initialized = true;
      
      // 触发一次全局或已有卡牌渲染
      document.dispatchEvent(new CustomEvent('glossaryReady'));
    } catch (err) {
      console.warn('[glossary] 术语库加载失败:', err);
    }
  }

  // 对指定 DOM 节点内的文本执行高亮绑定
  function applyGlossary(element) {
    if (!state.initialized || state.terms.length === 0 || !element) return;
    
    const terms = state.terms;
    
    // 递归替换文本节点
    function processNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        let text = node.nodeValue;
        let matches = [];
        
        terms.forEach((termInfo, termIdx) => {
          const word = termInfo.word;
          let index = text.indexOf(word);
          while (index !== -1) {
            // 确保不与已匹配的长句子重叠
            let overlap = false;
            for (let m of matches) {
              if (index < m.end && index + word.length > m.start) {
                overlap = true;
                break;
              }
            }
            if (!overlap) {
              matches.push({
                start: index,
                end: index + word.length,
                word: word,
                termIdx: termIdx
              });
            }
            index = text.indexOf(word, index + 1);
          }
        });
        
        if (matches.length > 0) {
          matches.sort((a, b) => a.start - b.start);
          
          const parent = node.parentNode;
          const fragment = document.createDocumentFragment();
          let lastIdx = 0;
          
          matches.forEach(m => {
            if (m.start > lastIdx) {
              fragment.appendChild(document.createTextNode(text.substring(lastIdx, m.start)));
            }
            
            const span = document.createElement('span');
            span.className = 'glossary-term';
            span.dataset.termIdx = m.termIdx;
            span.textContent = m.word;
            fragment.appendChild(span);
            
            lastIdx = m.end;
          });
          
          if (lastIdx < text.length) {
            fragment.appendChild(document.createTextNode(text.substring(lastIdx)));
          }
          
          parent.replaceChild(fragment, node);
        }
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        const skipTags = ['SCRIPT', 'STYLE', 'INPUT', 'TEXTAREA', 'SELECT', 'OPTION', 'BUTTON', 'A'];
        if (!skipTags.includes(node.tagName) && !node.classList.contains('glossary-term')) {
          const children = Array.from(node.childNodes);
          children.forEach(processNode);
        }
      }
    }

    processNode(element);
    
    // 绑定悬浮框逻辑
    element.querySelectorAll('.glossary-term').forEach(el => {
      el.addEventListener('mouseenter', (e) => {
        const termIdx = el.dataset.termIdx;
        const termInfo = terms[termIdx];
        if (!termInfo) return;
        
        const term = termInfo.term;
        const tooltipBox = state.tooltipBox;
        
        tooltipBox.innerHTML = `
          <div class="glossary-tooltip-header">
            ${escapeHtml(term.term)}
            <span class="glossary-tooltip-category">${escapeHtml(term.category || '规则')}</span>
          </div>
          <div class="glossary-tooltip-body">
            ${escapeHtml(term.author_explanation).replace(/\n/g, '<br>')}
          </div>
          ${term.examples && term.examples.length > 0 ? `
            <div class="glossary-tooltip-examples">
              <strong>例：</strong>${escapeHtml(term.examples[0].text)}
            </div>
          ` : ''}
        `;
        
        tooltipBox.style.display = 'block';
        const rect = el.getBoundingClientRect();
        const tooltipRect = tooltipBox.getBoundingClientRect();
        
        let top = window.scrollY + rect.top - tooltipRect.height - 8;
        let left = window.scrollX + rect.left + (rect.width - tooltipRect.width) / 2;
        
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
          left = window.innerWidth - tooltipRect.width - 10;
        }
        if (rect.top - tooltipRect.height < 10) {
          top = window.scrollY + rect.bottom + 8;
        }
        
        tooltipBox.style.top = top + 'px';
        tooltipBox.style.left = left + 'px';
      });
      
      el.addEventListener('mouseleave', () => {
        state.tooltipBox.style.display = 'none';
      });
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // 挂载到全局
  window.Glossary = {
    init: init,
    apply: applyGlossary,
    isReady: () => state.initialized
  };

  // 页面加载自动初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
