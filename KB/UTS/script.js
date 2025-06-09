// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const userInfoForm = document.getElementById('userInfoForm');
    const testSection = document.getElementById('testSection');
    const resultsSection = document.getElementById('resultsSection');
    const userForm = document.getElementById('userForm');
    const questionContainer = document.getElementById('questionContainer');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const currentQuestionEl = document.getElementById('currentQuestion');
    const totalQuestionsEl = document.getElementById('totalQuestions');
    const progressBar = document.getElementById('progressBar');
    const retakeTestBtn = document.getElementById('retakeTest');
    const downloadPDFBtn = document.getElementById('downloadPDF');
    
    // Test state
    let currentQuestionIndex = 0;
    let userAnswers = [];
    let userData = {};
    
    // Initialize total questions count
    totalQuestionsEl.textContent = mbtiQuestions.length;
    
    // Form submission - start test
    userForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Save user data
        userData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            date: new Date().toLocaleDateString()
        };
        
        // Hide user form and show test
        userInfoForm.classList.add('hidden');
        testSection.classList.remove('hidden');
        testSection.classList.add('animate-fade-in');
        
        // Load first question
        loadQuestion(currentQuestionIndex);
    });
    
    // Load a question
    function loadQuestion(index) {
        const question = mbtiQuestions[index];
        
        // Update progress
        currentQuestionEl.textContent = index + 1;
        progressBar.style.width = `${((index + 1) / mbtiQuestions.length) * 100}%`;
        
        // Show/hide previous button
        prevBtn.classList.toggle('hidden', index === 0);
        
        // Update next button text if last question
        if (index === mbtiQuestions.length - 1) {
            nextBtn.textContent = 'See Results';
        } else {
            nextBtn.textContent = 'Next';
        }
        
        // Create question HTML
        let optionsHtml = '';
        question.options.forEach((option, i) => {
            // Check if this option was previously selected
            const isChecked = userAnswers.some(a => 
                a.questionIndex === index && a.optionIndex === i);
            
            optionsHtml += `
                <div class="mb-3">
                    <label class="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition ${isChecked ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200'}">
                        <input type="radio" name="question-${index}" value="${i}" 
                               class="form-radio h-5 w-5 text-indigo-600" 
                               ${isChecked ? 'checked' : ''}>
                        <span class="ml-3 text-gray-700">${option.text}</span>
                    </label>
                </div>
            `;
        });
        
        questionContainer.innerHTML = `
            <h3 class="text-xl font-medium text-gray-800 mb-6">${question.question}</h3>
            <div class="space-y-3">
                ${optionsHtml}
            </div>
        `;
    }
    
    // Next button click
    nextBtn.addEventListener('click', function() {
        // Get selected answer
        const selectedOption = document.querySelector(`input[name="question-${currentQuestionIndex}"]:checked`);
        
        if (!selectedOption && currentQuestionIndex < mbtiQuestions.length - 1) {
            alert('Please select an answer before continuing.');
            return;
        }
        
        // Save answer
        if (selectedOption) {
            const existingAnswerIndex = userAnswers.findIndex(a => a.questionIndex === currentQuestionIndex);
            
            if (existingAnswerIndex >= 0) {
                userAnswers[existingAnswerIndex].optionIndex = parseInt(selectedOption.value);
            } else {
                userAnswers.push({
                    questionIndex: currentQuestionIndex,
                    optionIndex: parseInt(selectedOption.value)
                });
            }
        }
        
        // If last question, show results
        if (currentQuestionIndex === mbtiQuestions.length - 1) {
            showResults();
            return;
        }
        
        // Go to next question
        currentQuestionIndex++;
        loadQuestion(currentQuestionIndex);
    });
    
    // Previous button click
    prevBtn.addEventListener('click', function() {
        currentQuestionIndex--;
        loadQuestion(currentQuestionIndex);
    });
    
    // Show results
    function showResults() {
        // Calculate MBTI type
        const result = calculateMBTIType(userAnswers);
        
        // Hide test and show results
        testSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        resultsSection.classList.add('animate-fade-in');
        
        // Display results
        document.getElementById('mbtiType').textContent = result.type;
        document.getElementById('mbtiDescription').textContent = result.description;
        
        // Display type breakdown
        const breakdownHtml = `
            <div class="flex items-center justify-between">
                <span class="font-medium">Extraversion (E)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${result.confidence.EI.E}%"></div>
                </div>
                <span class="font-medium">${result.confidence.EI.E}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Introversion (I)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${result.confidence.EI.I}%"></div>
                </div>
                <span class="font-medium">${result.confidence.EI.I}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Sensing (S)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-green-600 h-2.5 rounded-full" style="width: ${result.confidence.SN.S}%"></div>
                </div>
                <span class="font-medium">${result.confidence.SN.S}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Intuition (N)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-green-600 h-2.5 rounded-full" style="width: ${result.confidence.SN.N}%"></div>
                </div>
                <span class="font-medium">${result.confidence.SN.N}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Thinking (T)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-yellow-600 h-2.5 rounded-full" style="width: ${result.confidence.TF.T}%"></div>
                </div>
                <span class="font-medium">${result.confidence.TF.T}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Feeling (F)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-yellow-600 h-2.5 rounded-full" style="width: ${result.confidence.TF.F}%"></div>
                </div>
                <span class="font-medium">${result.confidence.TF.F}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Judging (J)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-purple-600 h-2.5 rounded-full" style="width: ${result.confidence.JP.J}%"></div>
                </div>
                <span class="font-medium">${result.confidence.JP.J}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="font-medium">Perceiving (P)</span>
                <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div class="bg-purple-600 h-2.5 rounded-full" style="width: ${result.confidence.JP.P}%"></div>
                </div>
                <span class="font-medium">${result.confidence.JP.P}%</span>
            </div>
        `;
        
        document.getElementById('typeBreakdown').innerHTML = breakdownHtml;
        
        // Display detailed analysis
        const analysisHtml = `
            <p class="mb-4">Based on your responses and our Bayesian analysis, your personality type is <strong>${result.type}</strong>.</p>
            <p class="mb-4">${result.description}</p>
            <p class="mb-4">The Bayesian algorithm calculated your type by considering both your responses and general population statistics to determine the most probable personality type that matches your answers.</p>
            <p>Here's how you scored on each dimension:</p>
            <ul class="list-disc pl-5 mt-2 space-y-1">
                <li><strong>Extraversion (E) vs Introversion (I):</strong> You scored ${result.confidence.EI.E}% E and ${result.confidence.EI.I}% I</li>
                <li><strong>Sensing (S) vs Intuition (N):</strong> You scored ${result.confidence.SN.S}% S and ${result.confidence.SN.N}% N</li>
                <li><strong>Thinking (T) vs Feeling (F):</strong> You scored ${result.confidence.TF.T}% T and ${result.confidence.TF.F}% F</li>
                <li><strong>Judging (J) vs Perceiving (P):</strong> You scored ${result.confidence.JP.J}% J and ${result.confidence.JP.P}% P</li>
            </ul>
        `;
        
        document.getElementById('detailedAnalysis').innerHTML = analysisHtml;
        
        // Save results to user data
        userData.results = result;
    }
    
    // Retake test button
    retakeTestBtn.addEventListener('click', function() {
        // Reset test
        currentQuestionIndex = 0;
        userAnswers = [];
        
        // Hide results and show test
        resultsSection.classList.add('hidden');
        testSection.classList.remove('hidden');
        
        // Load first question
        loadQuestion(currentQuestionIndex);
    });
    
    // Download PDF button
    downloadPDFBtn.addEventListener('click', function() {
        generatePDF();
    });
    
    // Generate PDF report
    async function generatePDF() {
        // Load the jsPDF library dynamically
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Add title
        doc.setFontSize(22);
        doc.setTextColor(40, 40, 150);
        doc.text('MBTI Personality Assessment Report', 105, 20, { align: 'center' });
        
        // Add subtitle
        doc.setFontSize(12);
        doc.setTextColor(100, 100, 100);
        doc.text('Generated using Bayesian probability analysis', 105, 28, { align: 'center' });
        
        // Add line
        doc.setDrawColor(100, 100, 200);
        doc.setLineWidth(0.5);
        doc.line(20, 32, 190, 32);
        
        // Add user info
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Name: ${userData.name}`, 20, 42);
        doc.text(`Email: ${userData.email}`, 20, 50);
        if (userData.phone) doc.text(`Phone: ${userData.phone}`, 20, 58);
        doc.text(`Date: ${userData.date}`, 20, 66);
        
        // Add results section
        doc.setFontSize(16);
        doc.setTextColor(40, 40, 150);
        doc.text('Your Personality Results', 20, 80);
        
        doc.setFontSize(40);
        doc.setTextColor(80, 80, 200);
        doc.text(userData.results.type, 20, 95);
        
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(userData.results.description, 20, 105);
        
        // Add type breakdown
        doc.setFontSize(16);
        doc.setTextColor(40, 40, 150);
        doc.text('Type Breakdown', 20, 120);
        
        // Add dimension charts
        addDimensionChart(doc, 20, 130, 'Extraversion (E)', userData.results.confidence.EI.E, 'Introversion (I)', userData.results.confidence.EI.I);
        addDimensionChart(doc, 20, 150, 'Sensing (S)', userData.results.confidence.SN.S, 'Intuition (N)', userData.results.confidence.SN.N);
        addDimensionChart(doc, 20, 170, 'Thinking (T)', userData.results.confidence.TF.T, 'Feeling (F)', userData.results.confidence.TF.F);
        addDimensionChart(doc, 20, 190, 'Judging (J)', userData.results.confidence.JP.J, 'Perceiving (P)', userData.results.confidence.JP.P);
        
        // Add detailed analysis
        doc.addPage();
        doc.setFontSize(16);
        doc.setTextColor(40, 40, 150);
        doc.text('Detailed Analysis', 20, 20);
        
        const analysisText = [
            `Based on your responses and our Bayesian analysis, your personality type is ${userData.results.type}.`,
            userData.results.description,
            "The Bayesian algorithm calculated your type by considering both your responses and general population statistics to determine the most probable personality type that matches your answers.",
            "Here's how you scored on each dimension:",
            `- Extraversion (E) vs Introversion (I): You scored ${userData.results.confidence.EI.E}% E and ${userData.results.confidence.EI.I}% I`,
            `- Sensing (S) vs Intuition (N): You scored ${userData.results.confidence.SN.S}% S and ${userData.results.confidence.SN.N}% N`,
            `- Thinking (T) vs Feeling (F): You scored ${userData.results.confidence.TF.T}% T and ${userData.results.confidence.TF.F}% F`,
            `- Judging (J) vs Perceiving (P): You scored ${userData.results.confidence.JP.J}% J and ${userData.results.confidence.JP.P}% P`
        ];
        
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        let y = 30;
        analysisText.forEach(text => {
            const lines = doc.splitTextToSize(text, 170);
            doc.text(lines, 20, y);
            y += lines.length * 7;
        });
        
        // Save the PDF
        doc.save(`MBTI_Report_${userData.name.replace(' ', '_')}.pdf`);
    }
    
    // Helper function to add dimension chart to PDF
    function addDimensionChart(doc, x, y, label1, value1, label2, value2) {
        doc.setFontSize(10);
        doc.setTextColor(0, 0, 0);
        doc.text(label1, x, y);
        doc.text(`${value1}%`, x + 40, y);
        
        // Draw bar for first value
        doc.setFillColor(80, 80, 200);
        doc.rect(x + 50, y - 3, value1 * 1.2, 5, 'F');
        
        doc.text(label2, x, y + 8);
        doc.text(`${value2}%`, x + 40, y + 8);
        
        // Draw bar for second value
        doc.setFillColor(120, 120, 220);
        doc.rect(x + 50, y + 5, value2 * 1.2, 5, 'F');
    }
});