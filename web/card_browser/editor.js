let state = {
  activeTab: 'card',
  cards: [],
  selectedCard: null,
  documents: [],
  selectedDoc: null,
  stagedCandidates: {} // map of card_id -> candidate object
};

// 页面加载初始化
window.addEventListener('DOMContentLoaded', () => {
  switchTab('card');
  loadData();
  
  // 绑定类别更改的显示/隐藏处理
  document.getElementById('cardCategory').addEventListener('change', (e) => {
    updateFormFieldsByCategory(e.target.value);
  });
});

async function loadData() {
  await loadStagedCandidates();
  await loadCards();
  await loadDocuments();
}

// 切换标签页
function switchTab(tab) {
  state.activeTab = tab;
  
  // 更新导航按钮状态
  document.getElementById('tabCard').classList.toggle('active', tab === 'card');
  document.getElementById('tabDocs').classList.toggle('active', tab === 'docs');
  
  // 更新侧边栏面板状态
  document.getElementById('cardSidebar').classList.toggle('hidden', tab !== 'card');
  document.getElementById('docsSidebar').classList.toggle('hidden', tab !== 'docs');
  
  // 更新主编辑器面板状态
  document.getElementById('cardEditorPanel').classList.toggle('hidden', tab !== 'card');
  document.getElementById('docsEditorPanel').classList.toggle('hidden', tab !== 'docs');
}

// 消息提示组件
function notify(text, type = 'success') {
  const bar = document.getElementById('notifyBar');
  bar.textContent = text;
  bar.className = `notify-bar ${type}`;
  bar.classList.remove('hidden');
  setTimeout(() => {
    bar.classList.add('hidden');
  }, 4000);
}

// 读取当前已暂存的候选修改清单
async function loadStagedCandidates() {
  try {
    const res = await fetch('/api/change-candidates');
    if (!res.ok) throw new Error('获取暂存清单失败');
    const data = await res.json();
    
    state.stagedCandidates = {};
    const candidates = data.candidates || [];
    candidates.forEach(c => {
      // We map target card/doc ID to candidate record
      if (c.card_id) {
        state.stagedCandidates[c.card_id] = c;
      } else if (c.target_id) {
        state.stagedCandidates[c.target_id] = c;
      }
    });
    
    // 更新计数显示
    const count = Object.keys(state.stagedCandidates).length;
    document.getElementById('stagedCount').textContent = count;
  } catch (err) {
    console.error('Failed to load staged candidates:', err);
  }
}

// ==========================================
// 卡牌管理相关
// ==========================================

// 读取全量卡牌
async function loadCards() {
  const listEl = document.getElementById('cardList');
  listEl.innerHTML = '<div class="loading">读取卡牌中...</div>';
  try {
    const res = await fetch('/api/search?limit=1000');
    if (!res.ok) throw new Error('读取数据失败');
    const data = await res.json();
    state.cards = data.results || [];
    renderCardsList(state.cards);
  } catch (err) {
    listEl.innerHTML = `<div class="error">读取卡牌失败: ${err.message}</div>`;
  }
}

// 渲染卡牌列表
function renderCardsList(cards) {
  const listEl = document.getElementById('cardList');
  if (cards.length === 0) {
    listEl.innerHTML = '<div class="empty-state">没有找到卡牌</div>';
    return;
  }
  
  listEl.innerHTML = cards.map(card => {
    const isSelected = state.selectedCard && state.selectedCard.id === card.id;
    const isStaged = !!state.stagedCandidates[card.id];
    
    return `
      <div class="list-item ${isSelected ? 'active' : ''} ${isStaged ? 'staged-draft' : ''}" onclick="selectCard('${card.id}')">
        <div class="item-title">${escapeHtml(card.title)}</div>
        <div class="item-meta">
          <span class="badge badge-${card.category}">${escapeHtml(card.category_label)}</span>
          ${card.life ? `<span class="life-val">❤️ ${card.life}</span>` : ''}
        </div>
        ${isStaged ? '<span class="draft-indicator">📝 暂存草稿</span>' : ''}
      </div>
    `;
  }).join('');
}

// 卡牌筛选过滤
function filterCards() {
  const cat = document.getElementById('searchCategory').value;
  const q = document.getElementById('searchQ').value.toLowerCase().trim();
  const stagedOnly = document.getElementById('filterStagedOnly').checked;
  
  let filtered = state.cards;
  if (cat !== 'all') {
    filtered = filtered.filter(c => c.category === cat);
  }
  if (stagedOnly) {
    filtered = filtered.filter(c => !!state.stagedCandidates[c.id]);
  }
  if (q) {
    filtered = filtered.filter(c => 
      c.title.toLowerCase().includes(q) || 
      (c.source_work && c.source_work.toLowerCase().includes(q)) ||
      (c.author_group && c.author_group.toLowerCase().includes(q))
    );
  }
  renderCardsList(filtered);
}

// 选中并加载一张卡牌编辑
async function selectCard(id) {
  try {
    const res = await fetch(`/api/card/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error('加载卡牌详情失败');
    const card = await res.json();
    state.selectedCard = card;
    
    // 更新高亮样式
    renderCardsList(getActiveFilteredCards());
    
    // 渲染表单
    showCardForm(card);
  } catch (err) {
    notify(`加载失败: ${err.message}`, 'error');
  }
}

// 获取当前过滤条件下的卡牌列表
function getActiveFilteredCards() {
  const cat = document.getElementById('searchCategory').value;
  const q = document.getElementById('searchQ').value.toLowerCase().trim();
  const stagedOnly = document.getElementById('filterStagedOnly').checked;
  
  let filtered = state.cards;
  if (cat !== 'all') filtered = filtered.filter(c => c.category === cat);
  if (stagedOnly) filtered = filtered.filter(c => !!state.stagedCandidates[c.id]);
  if (q) filtered = filtered.filter(c => c.title.toLowerCase().includes(q));
  return filtered;
}

// 根据分类更新表单字段的可视性
function updateFormFieldsByCategory(category) {
  const isChar = category === 'combat_characters' || category === 'attached_characters' || category === 'deprecated';
  const isItem = category === 'items';
  
  document.querySelectorAll('.char-only').forEach(el => el.style.display = isChar ? 'flex' : 'none');
  document.querySelectorAll('.item-only').forEach(el => el.style.display = isItem ? 'flex' : 'none');
}

// 展现卡牌编辑表单
function showCardForm(card) {
  document.getElementById('cardEditorEmpty').classList.add('hidden');
  const form = document.getElementById('cardForm');
  form.classList.remove('hidden');
  
  // 检查是否有暂存的草稿内容覆盖它
  let displayCard = card;
  const staged = state.stagedCandidates[card.id];
  if (staged && staged.proposed_fields) {
    displayCard = {
      ...card,
      category: staged.category || card.category,
      title: staged.card_title || card.title,
      life: staged.proposed_fields.life ?? card.life,
      identity: staged.proposed_fields.identity ?? card.identity,
      gender: staged.proposed_fields.gender ?? card.gender,
      weapons: staged.proposed_fields.weapons ?? card.weapons,
      item_category: staged.proposed_fields.item_category ?? card.item_category,
      traits: staged.proposed_fields.traits ?? card.traits,
      source_work: staged.proposed_fields.source_work ?? card.source_work,
      author_group: staged.proposed_fields.author_group ?? card.author_group,
      relationships: staged.proposed_fields.relationships ?? card.relationships,
      description: staged.proposed_fields.description ?? card.description,
      abilities: staged.proposed_abilities ?? card.abilities
    };
  }
  
  // 填充基本字段
  document.getElementById('cardFormTitle').textContent = `编辑卡牌：${displayCard.title}`;
  document.getElementById('cardId').value = card.id || '';
  document.getElementById('originalCategory').value = card.category || '';
  document.getElementById('cardCategory').value = displayCard.category || 'combat_characters';
  document.getElementById('cardTitle').value = displayCard.title || '';
  document.getElementById('cardLife').value = displayCard.life || '';
  document.getElementById('cardIdentity').value = displayCard.identity || '';
  document.getElementById('cardGender').value = displayCard.gender || '男';
  document.getElementById('cardWeapons').value = displayCard.weapons || '';
  document.getElementById('cardItemCategory').value = displayCard.item_category || '';
  document.getElementById('cardTraits').value = displayCard.traits || '';
  document.getElementById('cardSourceWork').value = displayCard.source_work || '';
  document.getElementById('cardAuthorGroup').value = displayCard.author_group || '';
  document.getElementById('cardDesignGoal').value = staged ? (staged.design_goal || '') : '';
  document.getElementById('cardRelationships').value = displayCard.relationships || '';
  document.getElementById('cardDescription').value = displayCard.description || '';
  
  updateFormFieldsByCategory(displayCard.category || 'combat_characters');
  
  // 填充特技列表
  renderAbilities(displayCard.abilities || []);
}

// 新建卡牌
function createNewCard() {
  state.selectedCard = null;
  renderCardsList(getActiveFilteredCards());
  
  const dummyCard = {
    id: '',
    category: 'combat_characters',
    title: '新卡牌',
    life: 2000,
    gender: '男',
    weapons: '',
    source_work: '',
    author_group: '金庸',
    relationships: '',
    description: '',
    abilities: []
  };
  
  showCardForm(dummyCard);
  document.getElementById('cardTitle').focus();
}

// 取消编辑
function cancelCardEdit() {
  state.selectedCard = null;
  renderCardsList(getActiveFilteredCards());
  document.getElementById('cardForm').classList.add('hidden');
  document.getElementById('cardEditorEmpty').classList.remove('hidden');
}

// 动态特技处理
function renderAbilities(abilities) {
  const container = document.getElementById('abilitiesList');
  if (abilities.length === 0) {
    container.innerHTML = '<div class="no-abilities-hint">暂无特技数据，点击“添加特技”开始配置</div>';
    return;
  }
  
  container.innerHTML = abilities.map((ab, idx) => `
    <div class="ability-card" data-idx="${idx}">
      <div class="ability-row">
        <select class="ab-kind" onchange="syncAbilitiesToDescription()">
          <option value="招式" ${ab.kind === '招式' ? 'selected' : ''}>招式</option>
          <option value="内功" ${ab.kind === '内功' ? 'selected' : ''}>内功</option>
          <option value="身法" ${ab.kind === '身法' ? 'selected' : ''}>身法</option>
          <option value="武功" ${ab.kind === '武功' ? 'selected' : ''}>武功</option>
          <option value="技能" ${ab.kind === '技能' ? 'selected' : ''}>技能</option>
          <option value="符卡" ${ab.kind === '符卡' ? 'selected' : ''}>符卡</option>
          <option value="说明" ${ab.kind === '说明' ? 'selected' : ''}>说明</option>
          <option value="*" ${ab.kind === '*' ? 'selected' : ''}>*</option>
          <option value="字" ${ab.kind === '字' ? 'selected' : ''}>字</option>
        </select>
        <input type="text" class="ab-name" placeholder="特技名称" value="${escapeHtml(ab.name || '')}" oninput="syncAbilitiesToDescription()" />
        <div class="ability-actions-row">
          ${idx > 0 ? `<button type="button" class="btn-move" onclick="moveAbilityUp(${idx})" title="向上移动">🔼 上移</button>` : ''}
          ${idx < abilities.length - 1 ? `<button type="button" class="btn-move" onclick="moveAbilityDown(${idx})" title="向下移动">🔽 下移</button>` : ''}
          <button type="button" class="btn-remove-ability" onclick="removeAbility(${idx})">🗑️ 删除</button>
        </div>
      </div>
      <textarea class="ab-text" placeholder="特技具体说明内容..." rows="2" oninput="syncAbilitiesToDescription()">${escapeHtml(ab.text || ab.description || '')}</textarea>
    </div>
  `).join('');
}

// 添加一个空特技
function addAbility() {
  const abilities = collectAbilitiesFromForm();
  abilities.push({
    kind: '招式',
    name: '',
    text: ''
  });
  renderAbilities(abilities);
  syncAbilitiesToDescription();
}

// 删除一个特技
function removeAbility(index) {
  const abilities = collectAbilitiesFromForm();
  abilities.splice(index, 1);
  renderAbilities(abilities);
  syncAbilitiesToDescription();
}

// 向上移动特技顺序
function moveAbilityUp(index) {
  const abilities = collectAbilitiesFromForm();
  if (index > 0) {
    const temp = abilities[index];
    abilities[index] = abilities[index - 1];
    abilities[index - 1] = temp;
    renderAbilities(abilities);
    syncAbilitiesToDescription();
  }
}

// 向下移动特技顺序
function moveAbilityDown(index) {
  const abilities = collectAbilitiesFromForm();
  if (index < abilities.length - 1) {
    const temp = abilities[index];
    abilities[index] = abilities[index + 1];
    abilities[index + 1] = temp;
    renderAbilities(abilities);
    syncAbilitiesToDescription();
  }
}

// 收集表单里的特技结构数据
function collectAbilitiesFromForm() {
  const cards = [];
  const listEl = document.getElementById('abilitiesList');
  const cardsDom = listEl.querySelectorAll('.ability-card');
  cardsDom.forEach((cardEl) => {
    const kind = cardEl.querySelector('.ab-kind').value;
    const name = cardEl.querySelector('.ab-name').value.trim();
    const text = cardEl.querySelector('.ab-text').value.trim();
    cards.push({ kind, name, text });
  });
  return cards;
}

// 将结构化特技同步生成到原始文本框中
function syncAbilitiesToDescription() {
  const abilities = collectAbilitiesFromForm();
  let descLines = [];
  let lastKind = null;
  
  abilities.forEach((ab) => {
    let line = '';
    let kind = ab.kind || '招式';
    let name = ab.name || '';
    let text = ab.text || '';
    
    if (kind === '*') {
      line = `*${name}：${text}`;
    } else if (kind === '字' || (name.startsWith('【') && name.endsWith('】'))) {
      line = `${name}：${text}`;
    } else {
      if (kind !== lastKind) {
        line = `${kind}：${name}：${text}`;
        lastKind = kind;
      } else {
        line = `${name}：${text}`;
      }
    }
    descLines.push(line);
  });
  
  document.getElementById('cardDescription').value = descLines.join('\n\n');
}

// 保存卡牌候选修改（暂存修改）
async function saveCard(event) {
  event.preventDefault();
  
  const id = document.getElementById('cardId').value;
  const category = document.getElementById('cardCategory').value;
  const originalCategory = document.getElementById('originalCategory').value;
  const title = document.getElementById('cardTitle').value.trim();
  const designGoal = document.getElementById('cardDesignGoal').value.trim();
  
  if (!title) {
    notify('卡牌名称不能为空', 'error');
    return;
  }
  
  // 组装 fields
  const fields = {
    title: title,
    source_work: document.getElementById('cardSourceWork').value.trim(),
    author_group: document.getElementById('cardAuthorGroup').value.trim(),
    relationships: document.getElementById('cardRelationships').value.trim(),
    description: document.getElementById('cardDescription').value.trim()
  };
  
  const isChar = category === 'combat_characters' || category === 'attached_characters' || category === 'deprecated';
  if (isChar) {
    fields.life = Number(document.getElementById('cardLife').value) || 0;
    fields.identity = document.getElementById('cardIdentity').value.trim();
    fields.gender = document.getElementById('cardGender').value;
    fields.weapons = document.getElementById('cardWeapons').value.trim();
  } else if (category === 'items') {
    fields.item_category = document.getElementById('cardItemCategory').value.trim();
    fields.traits = document.getElementById('cardTraits').value.trim();
  }
  
  const abilities = collectAbilitiesFromForm();
  
  // We POST to the change-candidate save endpoint
  const payload = {
    card_id: id,
    category,
    original_category: originalCategory,
    title,
    design_goal: designGoal,
    fields,
    abilities
  };
  
  try {
    const res = await fetch('/api/change-candidate/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || '暂存失败');
    }
    
    const result = await res.json();
    notify(`卡牌《${title}》的修改已成功暂存到候选层！`);
    
    // 重新拉取暂存修改清单并渲染卡牌列表
    await loadStagedCandidates();
    await loadCards();
    
    // 继续选择正在编辑的卡牌
    selectCard(result.card_id || id);
  } catch (err) {
    notify(`暂存失败: ${err.message}`, 'error');
  }
}


// ==========================================
// 规则文献管理相关
// ==========================================

// 读取文档列表
async function loadDocuments() {
  const listEl = document.getElementById('docsList');
  listEl.innerHTML = '<div class="loading">读取文献中...</div>';
  try {
    const res = await fetch('/api/documents');
    if (!res.ok) throw new Error('读取数据失败');
    const data = await res.json();
    state.documents = data.documents || [];
    renderDocsList(state.documents);
  } catch (err) {
    listEl.innerHTML = `<div class="error">读取文献失败: ${err.message}</div>`;
  }
}

// 渲染文献列表
function renderDocsList(docs) {
  const listEl = document.getElementById('docsList');
  if (docs.length === 0) {
    listEl.innerHTML = '<div class="empty-state">没有文献记录</div>';
    return;
  }
  
  listEl.innerHTML = docs.map(doc => {
    const isSelected = state.selectedDoc && state.selectedDoc.id === doc.id;
    const isStaged = !!state.stagedCandidates[doc.id];
    
    return `
      <div class="list-item ${isSelected ? 'active' : ''} ${isStaged ? 'staged-draft' : ''}" onclick="selectDocument('${doc.id}')">
        <div class="item-title">${escapeHtml(doc.title)}</div>
        <div class="item-meta">
          <span class="badge">${escapeHtml(doc.group || '规则')}</span>
          <span class="version-label">v${escapeHtml(doc.version || '1.0')}</span>
        </div>
        ${isStaged ? '<span class="draft-indicator">📝 暂存草稿</span>' : ''}
      </div>
    `;
  }).join('');
}

// 选中并加载文献编辑
async function selectDocument(id) {
  try {
    const res = await fetch(`/api/document/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error('加载文献内容失败');
    const doc = await res.json();
    state.selectedDoc = doc;
    
    // 更新高亮样式
    renderDocsList(state.documents);
    
    // 展现文献表单
    document.getElementById('docsEditorEmpty').classList.add('hidden');
    const form = document.getElementById('docsForm');
    form.classList.remove('hidden');
    
    let displayContent = doc.content || '';
    const staged = state.stagedCandidates[doc.id];
    if (staged && staged.proposed_full_text) {
      displayContent = staged.proposed_full_text;
    }
    
    document.getElementById('docId').value = doc.id;
    document.getElementById('docFormTitle').textContent = `编辑文献：${doc.title}`;
    document.getElementById('docContent').value = displayContent;
  } catch (err) {
    notify(`加载失败: ${err.message}`, 'error');
  }
}

// 取消文献编辑
function cancelDocEdit() {
  state.selectedDoc = null;
  renderDocsList(state.documents);
  document.getElementById('docsForm').classList.add('hidden');
  document.getElementById('docsEditorEmpty').classList.remove('hidden');
}

// 暂存文献修改
async function saveDocument(event) {
  event.preventDefault();
  
  const id = document.getElementById('docId').value;
  const content = document.getElementById('docContent').value;
  
  const payload = {
    target_id: id,
    category: 'rules_text',
    title: state.selectedDoc.title,
    content: content,
    design_goal: '修改规则文档描述'
  };
  
  try {
    const res = await fetch('/api/change-candidate/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || '暂存失败');
    }
    
    notify('文献修改暂存成功！');
    
    // 重新拉取暂存修改清单并渲染文献列表
    await loadStagedCandidates();
    await loadDocuments();
    
    selectDocument(id);
  } catch (err) {
    notify(`暂存失败: ${err.message}`, 'error');
  }
}


// ==========================================
// 辅助函数
// ==========================================

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
