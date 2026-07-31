import { API_BASE_URL } from "../config/api";

export async function uploadDocument(file, selectedModels, summaryStyle) {
    const formData = new FormData();
    formData.append("file", file);
    selectedModels.forEach((model) => {
        formData.append("selected_models", model);
    });
    formData.append("summary_style", summaryStyle);
    const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData
    });
    if (!response.ok) {
        throw new Error("Failed to upload document.");
    }

    return await response.json();
}

export async function getJobStatus(jobId) {
    const response = await fetch(`${API_BASE_URL}/status/${jobId}`);
    if (!response.ok) {
        throw new Error("Failed to fetch job status.");
    }
    return await response.json();
}

export async function getResults(jobId) {
    const response = await fetch(`${API_BASE_URL}/results/${jobId}`);
    if (response.status === 404) {
        throw new Error("NOT_READY");
    }
    if (!response.ok) {
        throw new Error(`HTTP_${response.status}`);
    }
    return await response.json();
}

export async function downloadResults(jobId, format) {
    const response = await fetch(`${API_BASE_URL}/export/${jobId}?format=${format}`);
    if (!response.ok) {
        throw new Error(`Failed to download ${format}.`);
    }
    return await response.blob();
}