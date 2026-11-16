"""v16 templates (part 1): VIP SELLER HUB API (connect, balance, products + % markup import)."""
from templates_ui6 import TEMPLATES as T, ic  # noqa: F401

# ---- admin menu: new item next to the Tahir API System link
_old = '<a href="/admin/main-api" class="{{\'on\' if page==\'mapi\'}}">Tahir API System</a>'
assert _old in T["abase.html"]
T["abase.html"] = T["abase.html"].replace(
    _old, _old + '<a href="/admin/vsh" class="{{\'on\' if page==\'vsh\'}}">VIP Seller Hub</a>', 1)

VTABS = """<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 4px">
<a class=btn href="/admin/vsh" style="{{'' if page2=='c' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('key',16)}}Connection</a>
<a class=btn href="/admin/vsh/products" style="{{'' if page2=='p' else 'background:transparent;border:1px solid var(--bd);box-shadow:none'}}">{{ic('box',16)}}All Products</a></div>"""

T["admin_vsh.html"] = """{% extends 'abase.html' %}{% block c %}{% set page2='c' %}<h2>{{ic('code',24)}} VIP Seller Hub API</h2>""" + VTABS + """
<div class=card><h3>{{ic('key',20)}} Connect</h3>
<p class=mu>Paste your API token and press <b>Connect</b>. The Base URL is already filled in; change it only if your API link changes.</p>
<form method=post><input type=hidden name=action value=save>
<p class=mu>Base URL</p>
<input name=base value="{{base}}" autocomplete=off autocapitalize=off style="width:100%" required>
<p class=mu style="margin-top:10px">API Token{% if tail %} &mdash; saved (ends with <code>{{tail}}</code>). Leave empty to keep it.{% endif %}</p>
<input name=token type=password autocomplete=off placeholder="Paste your API token" style="width:100%" {{'' if tail else 'required'}}>
<p class=mu style="margin-top:10px">Price multiplier (1 = the prices on that site are already in {{CURRENCY}}; 90 = they are in USD and 1 USD = {{CURRENCY}}90)</p>
<input name=rate type=number step=any min=0.0001 value="{{rate|money}}" style="width:140px">
<br><button class=g style="margin-top:12px">{{ic('check')}} Connect</button></form></div>
<div class=card><h3>{{ic('wallet',20)}} Status &amp; Balance</h3>
{% if st %}{% if st.ok %}<span class="pill a">Connect successful</span>
{% if st.has_bal %}<div style="font-size:30px;font-weight:800;color:#34d399;margin:8px 0 2px">{{st.balance|cur}}</div>{% else %}<div class=mu style="margin:8px 0">Connected, but the balance field was not recognised - see the raw answer below and send it to me.</div>{% endif %}
{% else %}<span class="pill e">Not connected</span><div class=mu style="margin:8px 0">{{st.msg}}</div>{% endif %}
<div class=mu style="margin-top:6px">Last checked: {{st.ts|dt}}</div>
{% if st.raw %}<details style="margin-top:8px"><summary class=mu style="cursor:pointer">Raw answer (for testing)</summary><pre style="white-space:pre-wrap;word-break:break-all;font-size:12px">{{st.raw}}</pre></details>{% endif %}
{% else %}<div class=mu>Not checked yet. Paste your token and press Connect.</div>{% endif %}
<form method=post style="margin-top:12px"><input type=hidden name=action value=check><button>{{ic('wallet')}} Check Balance</button></form></div>
{% if st and st.ok %}<a class=btn href="/admin/vsh/products">{{ic('box',16)}} Open All Products &rarr;</a>{% endif %}
{% endblock %}"""

T["admin_vsh_products.html"] = """{% extends 'abase.html' %}{% block c %}{% set page2='p' %}<h2>{{ic('box',24)}} VIP Seller Hub &mdash; All Products</h2>""" + VTABS + """
{% if not cat %}<div class=card>No products yet. Connect the API first (Connection tab), then press Refresh.<br><br><a class=btn href="/admin/vsh/products?refresh=1">Refresh from API</a></div>
{% else %}
<form method=post>
<div class=card><div class=mu>Tick the products (or single plans) you want to sell, set your percentage, then press <b>Import selected</b>. Cost = the price on VIP Seller Hub.</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:12px">
<label class=mu>Reseller price = cost + <input name=mk_res id=mkr type=number step=any min=0 value="{{mr|money}}" style="width:80px"> %</label>
<label class=mu>User price = cost + <input name=mk_user id=mku type=number step=any min=0 value="{{mu|money}}" style="width:80px"> %</label></div>
<label class=mu style="display:block;margin-top:10px"><input type=checkbox name=overwrite> Also reset the prices of plans that are already imported</label>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
<button class=g name=scope value=sel>{{ic('plus')}} Import selected</button>
<button name=scope value=all onclick="return confirm('Import ALL products from VIP Seller Hub?')">{{ic('box')}} Import ALL</button>
<button type=submit name=scope value=sync class=o onclick="return confirm('Re-price every imported plan with fresh costs and these percentages?')">Sync prices</button>
<a class=btn href="/admin/vsh/products?refresh=1" style="background:transparent;border:1px solid var(--bd);box-shadow:none">Refresh</a>
<label class=mu style="margin-left:auto;display:flex;align-items:center;gap:6px"><input type=checkbox id=selall style="width:auto"> Select all</label></div>
<div class=mu style="margin-top:8px">List fetched: {{cat.ts|dt}} &middot; Edit single prices later in <a href="/admin/products">Products</a>.</div></div>
{% for g in groups %}<div class=card><div style="display:flex;justify-content:space-between;align-items:center"><h3>{{g.name}}</h3><label class=mu style="display:flex;align-items:center;gap:6px"><input type=checkbox class=ga style="width:auto"> all</label></div>
<div class=tw><table><tr><th></th><th>Plan</th><th>ID</th><th>Cost</th><th>Reseller</th><th>User</th><th>Status</th></tr>
{% for p in g.plans %}<tr><td><input type=checkbox name=pid value="{{p.pid}}" class=pc style="width:auto"></td><td>{{p.name}}{% if p.bala %} <span class="pill p">Bala Mod{% if p.mode %} {{p.mode}}{% endif %}</span>{% endif %}</td><td>{{p.pid}}</td>
<td>{{p.cost|cur}}</td><td class=rp data-c="{{p.cost}}">-</td><td class=up data-c="{{p.cost}}">-</td>
<td>{% if p.mine %}<span class="pill a">Imported</span> <span class=mu>R {{p.mine.price|cur}} / U {{p.mine.user_price|cur}}</span>{% else %}<span class="pill p">New</span>{% endif %}{% if not p.avail %} <span class="pill e">Out</span>{% endif %}</td></tr>{% else %}<tr><td colspan=7 class=mu>No plans</td></tr>{% endfor %}</table></div></div>
{% else %}<div class=card>The product list is empty. Press Refresh, or check the raw answer on the Connection tab.</div>{% endfor %}
</form>
<script>
const f2=v=>{v=Math.round(v*100)/100;return '{{CURRENCY}}'+v},mkr=document.getElementById('mkr'),mku=document.getElementById('mku');
function calc(){const a=parseFloat(mkr.value)||0,b=parseFloat(mku.value)||0;document.querySelectorAll('.rp').forEach(e=>e.textContent=f2(e.dataset.c*(1+a/100)));document.querySelectorAll('.up').forEach(e=>e.textContent=f2(e.dataset.c*(1+b/100)))}
mkr.oninput=mku.oninput=calc;calc();
document.querySelectorAll('.ga').forEach(g=>g.onchange=()=>g.closest('.card').querySelectorAll('.pc').forEach(c=>c.checked=g.checked));
document.getElementById('selall').onchange=function(){document.querySelectorAll('.pc,.ga').forEach(c=>c.checked=this.checked)};
</script>
{% endif %}{% endblock %}"""

TEMPLATES = T
