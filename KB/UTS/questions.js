const mbtiQuestions = [
    {
        question: "Saya lebih suka menghabiskan waktu bersama banyak orang daripada sendirian.",
        dimension: "EI",
        options: [
            { text: "Sangat tidak setuju", score: { I: 2 } },
            { text: "Tidak setuju", score: { I: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { E: 1 } },
            { text: "Sangat setuju", score: { E: 2 } }
        ]
    },
    {
        question: "Saya sering memikirkan kemungkinan-kemungkinan di masa depan daripada fokus pada fakta saat ini.",
        dimension: "SN",
        options: [
            { text: "Sangat tidak setuju", score: { S: 2 } },
            { text: "Tidak setuju", score: { S: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { N: 1 } },
            { text: "Sangat setuju", score: { N: 2 } }
        ]
    },
    {
        question: "Dalam mengambil keputusan, logika lebih penting daripada perasaan orang lain.",
        dimension: "TF",
        options: [
            { text: "Sangat tidak setuju", score: { F: 2 } },
            { text: "Tidak setuju", score: { F: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { T: 1 } },
            { text: "Sangat setuju", score: { T: 2 } }
        ]
    },
    {
        question: "Saya lebih suka ketika segala sesuatu terencana dengan baik daripada spontan.",
        dimension: "JP",
        options: [
            { text: "Sangat tidak setuju", score: { P: 2 } },
            { text: "Tidak setuju", score: { P: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { J: 1 } },
            { text: "Sangat setuju", score: { J: 2 } }
        ]
    },
    {
        question: "Bertemu orang baru membuat saya bersemangat daripada menguras energi.",
        dimension: "EI",
        options: [
            { text: "Sangat tidak setuju", score: { I: 2 } },
            { text: "Tidak setuju", score: { I: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { E: 1 } },
            { text: "Sangat setuju", score: { E: 2 } }
        ]
    },
    {
        question: "Saya lebih mempercayai pengalaman pribadi daripada teori yang belum teruji.",
        dimension: "SN",
        options: [
            { text: "Sangat tidak setuju", score: { N: 2 } },
            { text: "Tidak setuju", score: { N: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { S: 1 } },
            { text: "Sangat setuju", score: { S: 2 } }
        ]
    },
    {
        question: "Menjaga harmoni dalam kelompok lebih penting daripada selalu jujur.",
        dimension: "TF",
        options: [
            { text: "Sangat tidak setuju", score: { T: 2 } },
            { text: "Tidak setuju", score: { T: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { F: 1 } },
            { text: "Sangat setuju", score: { F: 2 } }
        ]
    },
    {
        question: "Saya lebih suka membuat daftar tugas daripada mengerjakan sesuatu secara spontan.",
        dimension: "JP",
        options: [
            { text: "Sangat tidak setuju", score: { P: 2 } },
            { text: "Tidak setuju", score: { P: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { J: 1 } },
            { text: "Sangat setuju", score: { J: 2 } }
        ]
    },
    {
        question: "Setelah acara sosial, saya butuh waktu sendiri untuk mengisi energi.",
        dimension: "EI",
        options: [
            { text: "Sangat tidak setuju", score: { E: 2 } },
            { text: "Tidak setuju", score: { E: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { I: 1 } },
            { text: "Sangat setuju", score: { I: 2 } }
        ]
    },
    {
        question: "Saya lebih fokus pada gambaran besar daripada detail-detail kecil.",
        dimension: "SN",
        options: [
            { text: "Sangat tidak setuju", score: { S: 2 } },
            { text: "Tidak setuju", score: { S: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { N: 1 } },
            { text: "Sangat setuju", score: { N: 2 } }
        ]
    },
    {
        question: "Kebenaran harus diutamakan meskipun menyakiti perasaan orang.",
        dimension: "TF",
        options: [
            { text: "Sangat tidak setuju", score: { F: 2 } },
            { text: "Tidak setuju", score: { F: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { T: 1 } },
            { text: "Sangat setuju", score: { T: 2 } }
        ]
    },
    {
        question: "Saya lebih suka pekerjaan dengan deadline jelas daripada jadwal fleksibel.",
        dimension: "JP",
        options: [
            { text: "Sangat tidak setuju", score: { P: 2 } },
            { text: "Tidak setuju", score: { P: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { J: 1 } },
            { text: "Sangat setuju", score: { J: 2 } }
        ]
    },
    {
        question: "Saya mudah memulai percakapan dengan orang asing.",
        dimension: "EI",
        options: [
            { text: "Sangat tidak setuju", score: { I: 2 } },
            { text: "Tidak setuju", score: { I: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { E: 1 } },
            { text: "Sangat setuju", score: { E: 2 } }
        ]
    },
    {
        question: "Saya lebih percaya pada hal-hal yang konkret dan bisa dibuktikan.",
        dimension: "SN",
        options: [
            { text: "Sangat tidak setuju", score: { N: 2 } },
            { text: "Tidak setuju", score: { N: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { S: 1 } },
            { text: "Sangat setuju", score: { S: 2 } }
        ]
    },
    {
        question: "Saya sering mempertimbangkan bagaimana keputusan saya mempengaruhi perasaan orang lain.",
        dimension: "TF",
        options: [
            { text: "Sangat tidak setuju", score: { T: 2 } },
            { text: "Tidak setuju", score: { T: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { F: 1 } },
            { text: "Sangat setuju", score: { F: 2 } }
        ]
    },
    {
        question: "Saya merasa tidak nyaman ketika rencana berubah di menit terakhir.",
        dimension: "JP",
        options: [
            { text: "Sangat tidak setuju", score: { P: 2 } },
            { text: "Tidak setuju", score: { P: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { J: 1 } },
            { text: "Sangat setuju", score: { J: 2 } }
        ]
    },
    {
        question: "Saya lebih memilih obrolan mendalam dengan satu orang daripada percakapan ringan dengan banyak orang.",
        dimension: "EI",
        options: [
            { text: "Sangat tidak setuju", score: { E: 2 } },
            { text: "Tidak setuju", score: { E: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { I: 1 } },
            { text: "Sangat setuju", score: { I: 2 } }
        ]
    },
    {
        question: "Saya tertarik pada ide-ide baru dan konsep-konsep inovatif.",
        dimension: "SN",
        options: [
            { text: "Sangat tidak setuju", score: { S: 2 } },
            { text: "Tidak setuju", score: { S: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { N: 1 } },
            { text: "Sangat setuju", score: { N: 2 } }
        ]
    },
    {
        question: "Keadilan lebih penting daripada belas kasihan dalam menyelesaikan masalah.",
        dimension: "TF",
        options: [
            { text: "Sangat tidak setuju", score: { F: 2 } },
            { text: "Tidak setuju", score: { F: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { T: 1 } },
            { text: "Sangat setuju", score: { T: 2 } }
        ]
    },
    {
        question: "Saya lebih suka membuat keputusan cepat daripada menimbang-nimbang terlalu lama.",
        dimension: "JP",
        options: [
            { text: "Sangat tidak setuju", score: { J: 2 } },
            { text: "Tidak setuju", score: { J: 1 } },
            { text: "Netral", score: {} },
            { text: "Setuju", score: { P: 1 } },
            { text: "Sangat setuju", score: { P: 2 } }
        ]
    }
];

// Prior probabilities tetap sama
const priorProbabilities = {
    E: 0.55, I: 0.45,
    S: 0.73, N: 0.27,
    T: 0.40, F: 0.60,
    J: 0.54, P: 0.46
};

// MBTI descriptions tetap sama
const mbtiDescriptions = {
    // ... (sama seperti sebelumnya)
};

// Fungsi calculateMBTIType perlu disesuaikan untuk menangani skor yang lebih granular
function calculateMBTIType(answers) {
    let scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
    
    answers.forEach(answer => {
        const question = mbtiQuestions[answer.questionIndex];
        const selectedOption = question.options[answer.optionIndex];
        
        // Update scores dengan Bayesian probability dan skor jawaban
        for (const [dimension, value] of Object.entries(selectedOption.score)) {
            scores[dimension] += value * priorProbabilities[dimension];
        }
    });
    
    // Normalisasi skor untuk memastikan konsistensi
    const normalize = (score, maxPossible) => {
        return (score / maxPossible) * 100;
    };
    
    // Max possible score (2 points per question * 5 questions per dimension * prior probability)
    const maxEI = 10 * 2 * Math.max(priorProbabilities.E, priorProbabilities.I);
    const maxSN = 10 * 2 * Math.max(priorProbabilities.S, priorProbabilities.N);
    const maxTF = 10 * 2 * Math.max(priorProbabilities.T, priorProbabilities.F);
    const maxJP = 10 * 2 * Math.max(priorProbabilities.J, priorProbabilities.P);
    
    const confidence = {
        EI: { 
            E: Math.round(normalize(scores.E, maxEI)),
            I: Math.round(normalize(scores.I, maxEI))
        },
        SN: { 
            S: Math.round(normalize(scores.S, maxSN)),
            N: Math.round(normalize(scores.N, maxSN))
        },
        TF: { 
            T: Math.round(normalize(scores.T, maxTF)),
            F: Math.round(normalize(scores.F, maxTF))
        },
        JP: { 
            J: Math.round(normalize(scores.J, maxJP)),
            P: Math.round(normalize(scores.P, maxJP))
        }
    };
    
    const type = [
        confidence.EI.E > confidence.EI.I ? 'E' : 'I',
        confidence.SN.S > confidence.SN.N ? 'S' : 'N',
        confidence.TF.T > confidence.TF.F ? 'T' : 'F',
        confidence.JP.J > confidence.JP.P ? 'J' : 'P'
    ].join('');
    
    return {
        type,
        description: mbtiDescriptions[type] || "Kepribadian unik dengan keseimbangan trait yang menarik.",
        confidence,
        scores
    };
}