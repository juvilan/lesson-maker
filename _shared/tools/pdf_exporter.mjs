#!/usr/bin/env node
/**
 * pdf_exporter.mjs
 * Puppeteer 기반 HTML → A4 PDF 변환 도구
 *
 * 사용법:
 *   node pdf_exporter.mjs --input <html_path> --output <pdf_path> [--format A4]
 *
 * 예시:
 *   node pdf_exporter.mjs --input output/worksheet_20260312.html --output output/worksheet_20260312.pdf
 */

import { readFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

function parseArgs(argv) {
  const args = {}
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2)
      args[key] = argv[i + 1] ?? true
      i++
    }
  }
  return args
}

async function exportToPdf({ inputPath, outputPath, format = 'A4' }) {
  // Puppeteer dynamic import (설치 여부에 따라 분기)
  let puppeteer
  try {
    puppeteer = await import('puppeteer')
    puppeteer = puppeteer.default ?? puppeteer
  } catch {
    throw new Error(
      'puppeteer가 설치되지 않았습니다.\n' +
      '설치: npm install puppeteer\n' +
      '또는: npx puppeteer install chrome'
    )
  }

  const absoluteInput = resolve(inputPath)
  if (!existsSync(absoluteInput)) {
    throw new Error(`입력 파일을 찾을 수 없습니다: ${absoluteInput}`)
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
  })

  try {
    const page = await browser.newPage()

    // 파일 로드 (file:// 프로토콜)
    const fileUrl = `file://${absoluteInput}`
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 })

    // MathJax 렌더링 대기 (최대 5초)
    try {
      await page.waitForFunction(
        () => typeof MathJax !== 'undefined' && MathJax.typesetPromise !== undefined,
        { timeout: 5000 }
      )
      await page.evaluate(() => MathJax.typesetPromise())
      // 렌더링 완료 후 추가 대기
      await new Promise(resolve => setTimeout(resolve, 500))
    } catch {
      // MathJax 없으면 스킵
    }

    // A4 PDF 생성
    const marginConfig = {
      top: '15mm',
      right: '15mm',
      bottom: '20mm',
      left: '15mm',
    }

    await page.pdf({
      path: resolve(outputPath),
      format,
      margin: marginConfig,
      printBackground: true,
      displayHeaderFooter: false,
      preferCSSPageSize: true,
    })

    console.log(`✅ PDF 생성 완료: ${resolve(outputPath)}`)
  } finally {
    await browser.close()
  }
}

// ── CLI 실행 ──
const args = parseArgs(process.argv)

if (!args.input || !args.output) {
  console.error('사용법: node pdf_exporter.mjs --input <html_path> --output <pdf_path> [--format A4]')
  process.exit(1)
}

exportToPdf({
  inputPath: args.input,
  outputPath: args.output,
  format: args.format ?? 'A4',
}).catch(err => {
  console.error('❌ PDF 변환 실패:', err.message)
  process.exit(1)
})
