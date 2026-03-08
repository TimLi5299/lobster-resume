// 作品数据 - 在这里添加你的作品！
// 每个作品包含以下字段：
// - id: 唯一编号
// - title: 标题
// - date: 创作日期
// - type: 类型（AI 绘画/AI 写作/AI 视频/AI 音乐/数据分析/其他）
// - cover: 封面图 URL（可以是本地路径或网络链接）
// - description: 作品描述/创作说明
// - aiTools: 使用的 AI 工具数组
// - tags: 标签数组

const works = [
    {
        id: 1,
        title: "未来城市 · AI 概念图",
        date: "2026-03-04",
        type: "AI 绘画",
        cover: "", // 填入图片链接，如 "images/work1.jpg"
        description: "用 Midjourney 生成的第一幅作品，主题是 2100 年的科技城市。prompt：futuristic city with flying cars, neon lights, cyberpunk style, ultra detailed, 8k",
        aiTools: ["Midjourney"],
        tags: ["测试作品", "赛博朋克", "城市"]
    },
    {
        id: 2,
        title: "AI 写的创业故事",
        date: "2026-03-03",
        type: "AI 写作",
        cover: "",
        description: "让 Claude 写的一个关于 AI 创业公司的短篇故事，探讨了人与 AI 的关系。",
        aiTools: ["Claude"],
        tags: ["故事", "创业", "思考"]
    },
    {
        id: 3,
        title: "公司财报数据分析",
        date: "2026-03-01",
        type: "数据分析",
        cover: "",
        description: "用 AI 分析了一家上市公司的财报，自动生成了关键指标和趋势图。",
        aiTools: ["GPT-4", "Python"],
        tags: ["金融", "数据分析", "自动化"]
    },
    // 复制上面的格式，添加更多作品...
];
