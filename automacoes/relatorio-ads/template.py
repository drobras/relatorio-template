import json,sys
# uso: python3 template.py dados.json saida.html
# dados.json: {"titulo_data":"15/10/2026","selo":"Dia anterior fechado","periodo":"Ontem","resumo_html":"...",
#  "kpis":[["Leads","1","Mês: 3","bom|ruim|normal"],...4 itens],
#  "p1":{"titulo":"Ontem","sub":"15/10","canais":{"Google Ads":{gasto,orc,imp,cli,conv},"Meta Ads":{...},"Total":{...}}},
#  "p2":{...7 dias, sem orc...},"p3":{...mês...},
#  "detalhe":{"sub":"...","linhas":[{"canal":"Google Ads","nome":"...","st":"Veiculando","gasto":0,"orc":0,"imp":0,"cli":0,"conv":0}]},
#  "termos":[["termo","campanha",imp,cli,gasto,conv]],"termos_sub":"Google Ads · DD/MM","alertas":[["vermelho|laranja|verde","texto html"]],
#  "saldo":{"valor":44.62,"pagamentos":100,"gasto":55.38,"desde":"13/10","media_dia":27.69,"dias":1.6,"recarregar_ate":"15/10","ultimo_pagamento":"13/10 · R$ 100,00"},
#  "negativas":{"sub":"...","total":6,"linhas":[["termo","FRASE|EXATA","motivo","aplicada|pendente|erro","DD/MM HH:MM"]]},
#  "contas_rodape":"(opcional) texto das contas no rodapé",
#  "analise_html":"texto html","acoes":[{"prioridade":"alta|media|baixa","acao":"...","quando":"Hoje|Até DD/MM|...","motivo":"..."}]}
d=json.load(open(sys.argv[1]))
def brl(v): return "—" if v is None else ("R$ "+f"{v:,.2f}").replace(",","X").replace(".",",").replace("X",".")
def pct(v,c=1): return "—" if v is None else f"{v*100:.{c}f}%".replace(".",",")
def num(v): return f"{int(round(v or 0)):,}".replace(",",".")
def met(c):
    g,i,k,cv,o=c.get("gasto") or 0,c.get("imp") or 0,c.get("cli") or 0,c.get("conv") or 0,c.get("orc") or 0
    return dict(c,gasto=g,imp=i,cli=k,conv=cv,pct=g/o if o else None,ctr=k/i if i else None,cpc=g/k if k else None,cpm=g/i*1000 if i else None,cpl=g/cv if cv else None)
NAVY="#0B2545";NAVY2="#13315C";OR="#F28C28";INK="#0F172A";MU="#475569";LN="#E2E8F0";BG="#EEF2F6";CARD="#FFFFFF";SOFT="#F8FAFC"
OK="#16A34A";BAD="#DC2626";WARN="#D97706"
CC={"Google Ads":"#1A73E8","Meta Ads":"#7C3AED","Total":NAVY}
F="font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;"
def sec(titulo,sub,corpo,pad="20px 22px"):
    s=f'<div style="{F}font-size:12px;color:{MU};margin:2px 0 14px;">{sub}</div>' if sub else ""
    return f'<tr><td style="padding:0 16px 16px;"><table width="100%" cellpadding="0" cellspacing="0" style="background:{CARD};border-radius:14px;border:1px solid {LN};"><tr><td style="padding:{pad};"><div style="{F}font-size:16px;font-weight:700;color:{INK};">{titulo}</div>{s}{corpo}</td></tr></table></td></tr>'
def bar(frac,cor,h=8,bg=LN):
    w=max(0,min(1,frac or 0))*100
    inner=f'<td width="{w:.0f}%" style="background:{cor};height:{h}px;border-radius:{h}px;font-size:0;line-height:0;">&nbsp;</td>' if w>=1 else ""
    rest=f'<td style="font-size:0;line-height:0;">&nbsp;</td>' if w<99 else ""
    return f'<table width="100%" cellpadding="0" cellspacing="0" style="background:{bg};border-radius:{h}px;height:{h}px;"><tr>{inner}{rest}</tr></table>'
def chip(t,cor): return f'<span style="{F}display:inline-block;font-size:11px;font-weight:700;color:{cor};background:{cor}1A;border-radius:20px;padding:3px 9px;white-space:nowrap;">{t}</span>'
def dot(c): return f'<span style="display:inline-block;width:9px;height:9px;border-radius:5px;background:{CC.get(c,NAVY)};margin-right:7px;vertical-align:middle;"></span>'
# ---------- KPIs
def kpi(r,v,s,t,*_):
    cor={"ruim":BAD,"bom":OK}.get(t,INK)
    return f'<div style="display:inline-block;vertical-align:top;width:48%;min-width:140px;max-width:155px;margin:0 0 10px;"><table width="96%" cellpadding="0" cellspacing="0" style="background:{CARD};border-radius:12px;border:1px solid {LN};"><tr><td style="padding:14px 14px 12px;{F}"><div style="font-size:11px;color:{MU};text-transform:uppercase;letter-spacing:.6px;font-weight:600;">{r}</div><div style="font-size:24px;font-weight:800;color:{cor};margin-top:6px;line-height:1.1;">{v}</div><div style="font-size:11px;color:{MU};margin-top:5px;">{s}</div></td></tr></table></div>'
kpis='<tr><td align="center" style="padding:0 12px 6px;font-size:0;">'+"".join(kpi(*k) for k in d["kpis"])+'</td></tr>'
# ---------- cartões por canal (período principal)
def canal_card(nome,c,com_orc):
    m=met(c); cor=CC[nome]
    def cel(l,v,extra=""): return f'<td width="50%" style="padding:8px 0;border-top:1px solid {LN};{F}"><div style="font-size:11px;color:{MU};">{l}</div><div style="font-size:15px;font-weight:700;color:{INK};margin-top:2px;">{v}</div>{extra}</td>'
    orc=""
    if com_orc and m.get("orc"):
        orc=f'<div style="{F}font-size:11px;color:{MU};margin:10px 0 5px;">{pct(m["pct"],0)} do orçamento diário de {brl(m["orc"])}</div>'+bar(m["pct"],cor)
    leadcor=OK if m["conv"]>0 else INK
    rows=(f'<tr>{cel("Impressões",num(m["imp"]))}{cel("Cliques",num(m["cli"]))}</tr>'
          f'<tr>{cel("CTR",pct(m["ctr"]))}{cel("CPC",brl(m["cpc"]))}</tr>'
          f'<tr>{cel("CPM",brl(m["cpm"]))}<td width="50%" style="padding:8px 0;border-top:1px solid {LN};{F}"><div style="font-size:11px;color:{MU};">Leads · CPL</div><div style="font-size:15px;font-weight:700;color:{leadcor};margin-top:2px;">{num(m["conv"])} <span style="color:{MU};font-weight:400;">·</span> <span style="color:{INK};">{brl(m["cpl"])}</span></div></td></tr>')
    return (f'<div style="display:inline-block;vertical-align:top;width:96%;max-width:276px;margin:0 4px 12px;text-align:left;"><table width="100%" cellpadding="0" cellspacing="0" style="background:{SOFT};border-radius:12px;border:1px solid {LN};border-top:4px solid {cor};"><tr><td style="padding:14px 16px 8px;text-align:left;">'
            f'<div style="{F}font-size:13px;font-weight:700;color:{cor};">{dot(nome)}{nome}</div>'
            f'<div style="{F}font-size:11px;color:{MU};margin-top:8px;">Investido</div><div style="{F}font-size:26px;font-weight:800;color:{INK};line-height:1.15;">{brl(m["gasto"])}</div>{orc}'
            f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px;">{rows}</table></td></tr></table></div>')
p1=d["p1"]
cards='<div style="text-align:center;font-size:0;">'+"".join(canal_card(n,p1["canais"][n],p1.get("com_orc")) for n in ["Google Ads","Meta Ads"] if n in p1["canais"])+'</div>'
# divisão do investimento
tot=met(p1["canais"].get("Total",{})); g=met(p1["canais"].get("Google Ads",{})); mm=met(p1["canais"].get("Meta Ads",{}))
div=""
if tot["gasto"]>0:
    fg=g["gasto"]/tot["gasto"]; fm=1-fg
    segs=(f'<td width="{fg*100:.0f}%" style="background:{CC["Google Ads"]};height:12px;font-size:0;">&nbsp;</td>' if fg>0.01 else "")+(f'<td width="{fm*100:.0f}%" style="background:{CC["Meta Ads"]};height:12px;font-size:0;">&nbsp;</td>' if fm>0.01 else "")
    div=(f'<div style="{F}font-size:12px;font-weight:700;color:{INK};margin:6px 0 8px;">Divisão do investimento · total {brl(tot["gasto"])}</div>'
         f'<table width="100%" cellpadding="0" cellspacing="0" style="border-radius:6px;overflow:hidden;"><tr>{segs}</tr></table>'
         f'<div style="{F}font-size:12px;color:{MU};margin-top:7px;">{dot("Google Ads")}Google {pct(fg,0)} &nbsp;&nbsp; {dot("Meta Ads")}Meta {pct(fm,0)}</div>')
sec_p1=sec(f'{p1["titulo"]} por canal',p1.get("sub",""),cards+div)
# ---------- funil (mês)
def funil(p):
    t=met(p["canais"]["Total"]); mx=max(t["imp"],1)
    linhas=[("Impressões",t["imp"],None,"#94A3B8"),("Cliques",t["cli"],t["ctr"],"#3B82F6"),("Leads",t["conv"],(t["conv"]/t["cli"] if t["cli"] else None),OK)]
    out=""
    for i,(l,v,taxa,cor) in enumerate(linhas):
        frac=max(v/mx,0.02) if v else 0.0
        tx=f' <span style="color:{MU};font-weight:400;">· {pct(taxa)} {"do anterior" if i else ""}</span>' if taxa is not None else ""
        out+=f'<tr><td style="padding:6px 0;{F}"><div style="font-size:12px;color:{INK};font-weight:700;margin-bottom:5px;">{l}: {num(v)}{tx}</div>{bar(frac,cor,10,SOFT)}</td></tr>'
    return f'<table width="100%" cellpadding="0" cellspacing="0">{out}</table><div style="{F}font-size:12px;color:{MU};margin-top:8px;">Custo por lead no período: <b style="color:{INK};">{brl(t["cpl"])}</b> · Investido: <b style="color:{INK};">{brl(t["gasto"])}</b></div>'
sec_funil=sec("Funil de conversão · mês",d["p3"].get("sub",""),funil(d["p3"])) if "p3" in d else ""
# ---------- comparativo de períodos
TH=f"{F}font-size:11px;color:{MU};font-weight:600;padding:8px 4px;border-bottom:1px solid {LN};text-align:right;"
def tdv(v,l=False,b=False,c=INK): return f'<td style="{F}font-size:12px;color:{c};padding:9px 4px;border-bottom:1px solid {LN};text-align:{"left" if l else "right"};{"font-weight:700;" if b else ""}">{v}</td>'
def tabela_periodo(p):
    h=f'<tr><th style="{TH}text-align:left;">Canal</th><th style="{TH}">Gasto</th><th style="{TH}">Cliques</th><th style="{TH}">Leads</th><th style="{TH}">CPL</th></tr>'
    b=""
    for k in ["Google Ads","Meta Ads","Total"]:
        if k not in p["canais"]: continue
        m=met(p["canais"][k]); T=k=="Total"
        b+=f'<tr style="{"background:"+SOFT+";" if T else ""}">'+tdv(dot(k)+k.replace(" Ads",""),True,T)+tdv(brl(m["gasto"]),b=T)+tdv(num(m["cli"])+f'<div style="font-size:10px;color:{MU};font-weight:400;">CTR {pct(m["ctr"])}</div>',b=T)+tdv(num(m["conv"]),b=True,c=OK if m["conv"] else INK)+tdv(brl(m["cpl"]),b=True)+'</tr>'
    return f'<div style="{F}font-size:13px;font-weight:700;color:{INK};margin:4px 0 2px;">{p["titulo"]} <span style="font-weight:400;color:{MU};font-size:12px;">· {p.get("sub","")}</span></div><table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:14px;">{h}{b}</table>'
sec_comp=sec("Comparativo de períodos","",( tabela_periodo(d["p2"]) if "p2" in d else "")+(tabela_periodo(d["p3"]) if "p3" in d else ""))
# ---------- campanhas
def camp(r):
    m=met(r); cor=CC.get(r["canal"],NAVY)
    stc={"Veiculando":OK}.get(r["st"],WARN)
    pc=m["pct"]; pcor=BAD if (pc or 0)>1 else cor
    orc=f'<div style="{F}font-size:11px;color:{MU};margin:8px 0 5px;">{brl(m["gasto"])} de {brl(m.get("orc"))} ({pct(pc,0)})</div>'+bar(pc,pcor,6) if m.get("orc") else f'<div style="{F}font-size:11px;color:{MU};margin-top:8px;">{brl(m["gasto"])} investidos</div>'
    stats=f'<div style="{F}font-size:12px;color:{MU};margin-top:8px;">{num(m["imp"])} impr. · {num(m["cli"])} cliques · CTR {pct(m["ctr"])} · <b style="color:{OK if m["conv"] else INK};">{num(m["conv"])} lead(s)</b></div>'
    return (f'<tr><td style="padding:12px 0;border-top:1px solid {LN};"><table width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td style="{F}font-size:14px;font-weight:700;color:{INK};">{dot(r["canal"])}{r["nome"]}</td><td align="right" style="white-space:nowrap;">{chip(r["st"],stc)}</td></tr></table>{orc}{stats}</td></tr>')
det=d["detalhe"]
def grupo(cn):
    rs=sorted([r for r in det["linhas"] if r["canal"]==cn],key=lambda r:-(r.get("gasto") or 0))
    if not rs: return ""
    tg=sum(r.get("gasto") or 0 for r in rs); tl=sum(r.get("conv") or 0 for r in rs)
    rot="campanha" if cn=="Google Ads" else "conjunto"
    head=(f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:6px;background:{CC[cn]}12;border-radius:8px;"><tr>'
          f'<td style="{F}font-size:13px;font-weight:800;color:{CC[cn]};padding:9px 12px;">{dot(cn)}{cn} <span style="font-weight:400;color:{MU};font-size:12px;">· {len(rs)} {rot}{"s" if len(rs)>1 else ""}</span></td>'
          f'<td align="right" style="{F}font-size:12px;color:{INK};padding:9px 12px;white-space:nowrap;"><b>{brl(tg)}</b> · {num(tl)} lead(s)</td></tr></table>')
    return head+f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:10px;">{"".join(camp(r) for r in rs)}</table>'
sec_det=sec(det.get("titulo","Campanhas e conjuntos"),det.get("sub",""),grupo("Google Ads")+grupo("Meta Ads"))
# ---------- termos
sec_termos=""
if d.get("termos"):
    ts=sorted(d["termos"],key=lambda t:-(t[4] or 0))
    h=f'<tr><th style="{TH}text-align:left;">Termo pesquisado</th><th style="{TH}">Impr.</th><th style="{TH}">Cliques</th><th style="{TH}">Gasto</th><th style="{TH}">Conv.</th></tr>'
    b="".join('<tr>'+f'<td style="{F}font-size:13px;color:{INK};padding:9px 6px;border-bottom:1px solid {LN};">{t[0]}<div style="font-size:11px;color:{MU};">{t[1]}</div></td>'+tdv(num(t[2]))+tdv(num(t[3]))+tdv(brl(t[4]),b=True)+tdv(num(t[5] if len(t)>5 else 0),b=True,c=OK if (len(t)>5 and t[5]) else MU)+'</tr>' for t in ts)
    sg=sum(t[4] or 0 for t in ts); sc=sum((t[5] if len(t)>5 else 0) or 0 for t in ts); sem=sum(t[4] or 0 for t in ts if not (len(t)>5 and t[5]))
    b+=f'<tr style="background:{SOFT};">'+tdv(f"Total · {len(ts)} termo(s)",True,True)+tdv(num(sum(t[2] or 0 for t in ts)),b=True)+tdv(num(sum(t[3] or 0 for t in ts)),b=True)+tdv(brl(sg),b=True)+tdv(num(sc),b=True,c=OK if sc else INK)+'</tr>'
    nota=f'<div style="{F}font-size:12px;color:{MU};margin-top:10px;">Gasto em termos sem conversão: <b style="color:{BAD if sem else INK};">{brl(sem)}</b> ({pct(sem/sg if sg else None,0)} do total). Termos fora do perfil de cliente viram palavras negativas automaticamente (ver seção ao fim).</div>'
    sec_termos=sec("Termos de pesquisa com gasto",d.get("termos_sub","Google Ads"),f'<table width="100%" cellpadding="0" cellspacing="0">{h}{b}</table>{nota}')
# ---------- negativas automáticas
sec_neg=""
ng=d.get("negativas")
if ng is not None:
    STN={"aplicada":("Aplicada",OK),"pendente":("Na fila",WARN),"erro":("Erro",BAD)}
    def lneg(x):
        termo,corr,motivo,status,data=(list(x)+["","","","",""])[:5]
        rot,cor=STN.get(status,(status,MU))
        fmt=f'[{termo}]' if corr=="EXATA" else f'"{termo}"'
        return (f'<tr><td style="padding:10px 0;border-top:1px solid {LN};{F}"><table width="100%" cellpadding="0" cellspacing="0"><tr>'
                f'<td style="{F}font-size:14px;font-weight:700;color:{INK};">{fmt} <span style="font-size:11px;font-weight:400;color:{MU};">{"exata" if corr=="EXATA" else "frase"}</span></td>'
                f'<td align="right" style="white-space:nowrap;vertical-align:top;padding-left:8px;">{chip(rot,cor)}</td></tr></table>'
                f'<div style="font-size:12px;color:#334155;margin-top:3px;line-height:1.5;">{motivo}{" · "+data if data else ""}</div></td></tr>')
    linhas=ng.get("linhas") or []
    corpo=(f'<table width="100%" cellpadding="0" cellspacing="0">{"".join(lneg(x) for x in linhas)}</table>' if linhas else
           f'<div style="{F}font-size:13px;color:{INK};">Nenhuma palavra negativa nova neste período — os termos analisados estão dentro do perfil de cliente.</div>')
    corpo+=(f'<div style="{F}font-size:11px;color:{MU};margin-top:10px;line-height:1.5;">Lista "CLAUDE | Negativas automáticas" · total aplicado: <b style="color:{INK};">{num(ng.get("total"))}</b>. '
            f'"Na fila" entra no Google Ads em até 1 hora. Para desfazer, remova o termo da lista no Google Ads ou peça ao Claude.</div>')
    sec_neg=sec("Palavras-chave negativas adicionadas",ng.get("sub",""),corpo)
# ---------- alertas
sec_al=""
if d.get("alertas"):
    cmap={"vermelho":BAD,"laranja":WARN,"verde":OK}
    sec_al=sec("Alertas","","".join(f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px;"><tr><td style="background:{cmap.get(c,WARN)}12;border-left:4px solid {cmap.get(c,WARN)};border-radius:8px;padding:10px 12px;{F}font-size:13px;color:{INK};line-height:1.5;">{t}</td></tr></table>' for c,t in d["alertas"]))
# ---------- saldo Google Ads
sec_saldo=""
sd=d.get("saldo")
if sd:
    v=sd.get("valor") or 0; dias=sd.get("dias"); med=sd.get("media_dia")
    cor=BAD if (dias is not None and dias<2) or v<=0 else (WARN if dias is not None and dias<4 else OK)
    st={BAD:"Recarregar agora",WARN:"Recarregar em breve",OK:"Saldo suficiente"}[cor]
    frac=min(1,(dias or 0)/10) if dias is not None else 0
    dtxt=(f'{str(round(dias,1)).replace(".",",")} dia(s)' if dias is not None else "—")
    corpo=(f'<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="{F}vertical-align:top;">'
           f'<div style="font-size:11px;color:{MU};">Saldo estimado agora</div><div style="font-size:28px;font-weight:800;color:{cor};line-height:1.15;">{brl(v)}</div></td>'
           f'<td align="right" style="vertical-align:top;">{chip(st,cor)}</td></tr></table>'
           f'<div style="{F}font-size:12px;color:{INK};margin:10px 0 6px;">Dura cerca de <b>{dtxt}</b> no ritmo atual ({brl(med)}/dia)'
           f'{" · recarregar até <b>"+sd["recarregar_ate"]+"</b>" if sd.get("recarregar_ate") else ""}</div>'+bar(frac,cor,8)+
           f'<div style="{F}font-size:11px;color:{MU};margin-top:8px;line-height:1.5;">Pagamentos desde {sd.get("desde","")}: <b>{brl(sd.get("pagamentos"))}</b> · gasto no período: <b>{brl(sd.get("gasto"))}</b>'
           f'{" · último pagamento: "+sd["ultimo_pagamento"] if sd.get("ultimo_pagamento") else ""}<br>Estimativa pelo gasto registrado; o valor oficial fica em Google Ads › Faturamento › Fundos disponíveis.</div>')
    sec_saldo=sec("Saldo Google Ads (pré-pago)","",corpo)
# ---------- análise e plano de ação
PCOR={"alta":BAD,"media":WARN,"média":WARN,"baixa":OK}
def acao(a):
    p=(a.get("prioridade") or "media").lower(); c=PCOR.get(p,WARN)
    return (f'<tr><td style="padding:10px 0;border-top:1px solid #FED7AA;{F}">'
            f'<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="{F}font-size:14px;font-weight:700;color:{INK};">{a.get("acao","")}</td>'
            f'<td align="right" style="white-space:nowrap;vertical-align:top;padding-left:8px;"><span style="{F}display:inline-block;font-size:11px;font-weight:700;color:#FFFFFF;background:#C2410C;border-radius:20px;padding:3px 9px;">{a.get("quando","")}</span></td></tr></table>'
            f'<div style="font-size:12px;color:#334155;margin-top:4px;line-height:1.5;"><span style="display:inline-block;width:8px;height:8px;border-radius:4px;background:{c};margin-right:6px;"></span>{a.get("motivo","")}</div></td></tr>')
an=d.get("analise_html") or d.get("recomendacao","")
acs=d.get("acoes") or []
sec_rec=(f'<tr><td style="padding:0 16px 16px;"><table width="100%" cellpadding="0" cellspacing="0" bgcolor="#FFF7ED" style="background:#FFF7ED;border-radius:14px;border:1px solid #FED7AA;border-left:6px solid {OR};"><tr><td bgcolor="#FFF7ED" style="padding:18px 22px;{F}">'
         f'<div style="font-size:12px;color:#C2410C;font-weight:800;letter-spacing:1px;text-transform:uppercase;">Análise e plano de ação</div>'
         f'<div style="font-size:14px;color:{INK};line-height:1.6;margin-top:6px;">{an}</div>'
         +(f'<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px;">{"".join(acao(a) for a in acs)}</table>' if acs else "")+
         f'<div style="font-size:11px;color:{MU};margin-top:10px;">Prioridade: <span style="color:{BAD};">●</span> alta · <span style="color:{WARN};">●</span> média · <span style="color:{OK};">●</span> baixa. Sugestões — além das negativas automáticas, nada é aplicado sem a sua aprovação.</div></td></tr></table></td></tr>')
selo=d.get("selo","")
html=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Relatório de anúncios</title></head>
<body style="margin:0;padding:0;background:{BG};">
<div style="display:none;max-height:0;overflow:hidden;">{d.get("preheader","")}</div>
<table width="100%" cellpadding="0" cellspacing="0" style="background:{BG};"><tr><td align="center" style="padding:24px 8px;">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:660px;">
<tr><td style="padding:0 16px 16px;"><table width="100%" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" style="background:#FFFFFF;border-radius:16px;border:1px solid {LN};border-top:6px solid {NAVY};"><tr><td bgcolor="#FFFFFF" style="padding:22px 24px 22px;{F}">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="{F}font-size:13px;font-weight:800;color:{NAVY};letter-spacing:.5px;">DR. OBRAS <span style="color:{OR};">●</span> <span style="font-weight:400;color:{MU};">Projetos e Construções</span></td>
<td align="right">{chip(selo,OR) if selo else ""}</td></tr></table>
<div style="font-size:26px;font-weight:800;color:{NAVY};margin-top:16px;line-height:1.2;">Relatório de anúncios</div>
<div style="font-size:14px;color:{MU};margin-top:4px;">{d["titulo_data"]} · Google Ads + Meta Ads</div>
<div style="height:3px;width:56px;background:{OR};border-radius:3px;margin-top:14px;font-size:0;">&nbsp;</div>
<div style="font-size:14px;color:{INK};line-height:1.6;margin-top:14px;">{d["resumo_html"]}</div>
</td></tr></table></td></tr>
{kpis}{sec_saldo}{sec_p1}{sec_al}{sec_rec}{sec_det}{sec_comp}{sec_funil}{sec_termos}{sec_neg}
<tr><td style="padding:4px 28px 28px;{F}font-size:11px;color:{MU};line-height:1.6;text-align:center;">
CTR = cliques ÷ impressões · CPC = gasto ÷ cliques · CPM = custo por mil impressões · CPL = gasto ÷ leads<br>
Lead no Meta = conversa iniciada no WhatsApp · Lead no Google = conversão (pedido de orçamento)<br>
{(d["contas_rodape"]+" · ") if d.get("contas_rodape") else ""}Relatório automático do Claude · única alteração automática: palavras-chave negativas</td></tr>
</table></td></tr></table></body></html>'''
open(sys.argv[2],"w").write(html); print(len(html))
