const cheerio = require('cheerio');
const fs = require('node:fs');


const baseUrl = 'https://www.degiro.com';


const sections = [
  '/uk/helpdesk/about-degiro',
  '/uk/helpdesk/account-and-personal-details',
  '/uk/helpdesk/become-client',
  '/uk/helpdesk/fees',
  '/uk/helpdesk/money-transfers-and-handling',
  '/uk/helpdesk/orders',
  '/uk/helpdesk/trading-platform',
  '/uk/helpdesk/trading-possibilities',
  '/uk/helpdesk/tax'
]

const extract = async (section) => {
  const data = [];
  const body = await (await fetch(baseUrl + section)).text()
  const $ = cheerio.load(body);

  let rows = $('.faq--row a')
    .toArray();

  for (const row of rows) {
    let link = row.attribs.href;
    let subBody = await (await fetch(baseUrl + link)).text();

    const $$ = cheerio.load(subBody);

    const content = $$('article').text()
      .replace('Answer', '')
      .trim()
      .replace(/\s{3}/g, '')
      .replace('Accordion', '')
      .trim()

    let resultString =
      `# ${$(row).text()}\n
## ${link}\n
${content}\n
`
    data.push(resultString);
  }

  return data;
}

const allData = [];

(async () => {
  for (const section of sections) {
    extract(section).then(result => {
      allData.push(...result);
    })

    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  try {
    const stream = fs.createWriteStream('../faq.md', {flags: 'a'});

    allData.forEach(d => stream.write(d))

    stream.end()
  } catch (err) {
    console.error(err);
  }
})()