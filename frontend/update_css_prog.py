with open("styles.css", "a", encoding="utf-8") as f:
    f.write("""
/* Progress Bar UI */
.progress-container {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
    gap: 12px;
    animation: fadeIn 0.3s ease-out;
}

.progress-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: #1f2937;
}

.progress-time {
    color: #3b82f6;
    background-color: rgba(59, 130, 246, 0.1);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
}

.progress-bar-bg {
    width: 100%;
    height: 12px;
    background-color: #e5e7eb;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
}

.progress-bar-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #3b82f6, #60a5fa, #3b82f6);
    background-size: 200% 100%;
    border-radius: 10px;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: gradientMove 2s linear infinite;
}

.progress-percent {
    text-align: right;
    font-size: 0.85rem;
    color: #6b7280;
    font-weight: 700;
}

@keyframes gradientMove {
    0% { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
""")
