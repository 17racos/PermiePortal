// Node script to migrate ERB HTML views into MDX articles
// Usage: node scripts/migrate-erb.cjs

const { readFileSync, writeFileSync, mkdirSync } = require('fs');
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

function migrateList(list, tagsArray){
  for(const rel of list){
    const srcPath = `${OLD}/${rel}`;
    let html; try { html = readFileSync(srcPath, 'utf8'); } catch(e){ console.error('skip missing:', rel); continue; }
    const noErb = stripErb(html);
    const h1 = firstH1(noErb);
    const base = basename(rel).replace(/\.html\.erb$/i,'');
    const slug = toSlug(base);
    const title = h1 || toTitle(slug);
    const date = lastGitDate(rel);
    const summary = summarize(stripTags(noErb));
    const body = noErb.trim();

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
    writeFileSync(`${OUTDIR}/${slug}.mdx`, fm + body, 'utf8');
    console.log(`migrated: ${rel} -> ${OUTDIR}/${slug}.mdx`);
  }
}

migrateList(rotten, ['satire','permaculture']);
migrateList(guides, ['guide','permaculture']);
