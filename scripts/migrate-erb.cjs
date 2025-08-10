// Node script to migrate ERB HTML views into MDX articles
// Usage: node scripts/migrate-erb.cjs

const { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync } = require('fs');
const { basename } = require('path');
const { execSync } = require('child_process');

const OLD = '/home/dracos/apps/permieportal_old';
const OUTDIR = '/home/dracos/apps/permieportal/src/content/articles';

const rotten = [
  'app/views/rotten_articles/great_american_lawn.html.erb',
  'app/views/rotten_articles/we-saved-the-lake-by-killing-it.html.erb',
  'app/views/rotten_articles/genghis-kahn-historys-greatest-environmentalist.html.erb',
];
const guides = [
  'app/views/guides/vermicomposting.html.erb',
  'app/views/guides/how-to-make-a-worm-bin.html.erb',
  'app/views/guides/plant-families.html.erb',
  'app/views/guides/turmeric-informational.html.erb',
  'app/views/guides/importance-of-soil-biodiversity.html.erb',
  'app/views/guides/moringa-informational.html.erb',
  'app/views/guides/unlocking-natures-blueprint.html.erb',
];

function stripErb(html){ return html.replace(/<%[\s\S]*?%>/g, ''); }
function stripTags(html){ return html.replace(/<[^>]+>/g, ''); }
function firstH1(html){ const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i); return m ? stripTags(m[1]).trim() : ''; }
function toTitle(slug){ return slug.replace(/[-_]+/g, ' ').replace(/\b\w/g, c=>c.toUpperCase()); }
function toSlug(name){ return name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,''); }
function lastGitDate(rel){ try { const out = execSync(`git -C ${OLD} log -1 --format=%cI -- ${rel}`, {encoding:'utf8', stdio:['ignore','pipe','ignore']}).trim(); return out || new Date().toISOString(); } catch(e){ return new Date().toISOString(); } }
function summarize(text){ const clean = text.replace(/\s+/g,' ').trim(); return clean.slice(0,160); }

function extractBody(html){
  // Remove DOCTYPE
  let h = html.replace(/<!DOCTYPE[^>]*>/ig, '');
  // Grab <body> content if present
  const m = h.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  if (m) { h = m[1]; }
  // Drop any remaining <head> blocks and <html> tags
  h = h.replace(/<head[\s\S]*?<\/head>/ig, '');
  h = h.replace(/<\/?.?html[^>]*>/ig, '');
  // Remove style blocks embedded in content
  h = h.replace(/<style[\s\S]*?<\/style>/ig, '');
  return h.trim();
}

function copyAssetIfExists(srcPath){
  // Try common old locations for assets
  const fname = srcPath.split('/').pop();
  const candidates = [
    `${OLD}/public/assets/${fname}`,
    `${OLD}/app/assets/images/${fname}`,
    `${OLD}/app/assets/${fname}`
  ];
  const dest = `/home/dracos/apps/permieportal/public/assets/${fname}`;
  for (const c of candidates){
    if (existsSync(c)){
      mkdirSync('/home/dracos/apps/permieportal/public/assets', { recursive: true });
      copyFileSync(c, dest);
      return `/assets/${fname}`;
    }
  }
  return srcPath; // leave as-is if not found
}

function rewriteImagesAndCopy(bodyHtml){
  let h = bodyHtml.replace(/<img([^>]+)src=["']([^"']+)["']([^>]*)>/ig, (full, pre, src, post) => {
    let newSrc = src;
    if (src.startsWith('/assets/')){
      newSrc = copyAssetIfExists(src);
    }
    // Ensure self-closing
    return `<img${pre}src="${newSrc}"${post} />`;
  });
  // Self-close common void tags for MDX/JSX compliance
  h = h.replace(/<br\s*>/ig, '<br />');
  h = h.replace(/<hr\s*>/ig, '<hr />');
  return h;
}

function normalizeParagraphs(html){
  let h = html.replace(/<p[^>]*>/ig, '');
  h = h.replace(/<\/p>/ig, '\n\n');
  // Remove trailing spaces on lines and collapse 3+ newlines to 2
  h = h.replace(/[\t ]+$/gm, '');
  h = h.replace(/\n{3,}/g, '\n\n');
  return h;
}

function migrateList(list, tagsArray){
  for(const rel of list){
    const srcPath = `${OLD}/${rel}`;
    let html; try { html = readFileSync(srcPath, 'utf8'); } catch(e){ console.error('skip missing:', rel); continue; }
    const noErb = stripErb(html);
    // Compute a cleaned body first (no head/style/doctype)
    let body = extractBody(noErb);
    // Use body for title/summary to avoid CSS text
    const h1 = firstH1(body);
    const base = basename(rel).replace(/\.html\.erb$/i,'');
    const slug = toSlug(base);
    const title = h1 || toTitle(slug);
    const date = lastGitDate(rel);
    let summary = summarize(stripTags(body));
    body = rewriteImagesAndCopy(body);
    body = normalizeParagraphs(body);
    // Sanitize any stray MDX expression braces
    body = body.replace(/\{/g, '&#123;').replace(/\}/g, '&#125;');
    summary = summary.replace(/\{/g, '(').replace(/\}/g, ')');

    const fm = [
      '---',
      `title: ${title}`,
      `date: ${date}`,
      `summary: "${summary.replace(/"/g,'\\"')}"`,
      `tags: ${JSON.stringify(tagsArray)}`,
      `slug: ${slug}`,
      '---',
      '',
    ].join('\n');

    mkdirSync(OUTDIR, { recursive: true });
    writeFileSync(`${OUTDIR}/${slug}.mdx`, fm + body + '\n', 'utf8');
    console.log(`migrated: ${rel} -> ${OUTDIR}/${slug}.mdx`);
  }
}

migrateList(rotten, ['satire','permaculture']);
migrateList(guides, ['guide','permaculture']);
