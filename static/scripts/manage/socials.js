function removeTrailingSlash(str) {
    // Check if the string ends with a slash and remove it if it does
    return str.endsWith('/') ? str.slice(0, -1) : str;
}


function checkInputs() {
    const urlPatterns = {
        facebook: /^https:\/\/(www\.)?facebook.com\/[a-zA-Z0-9(\.\?)?]/,
        instagram: /^https:\/\/(www\.)?instagram.com\/[a-zA-Z0-9_]+$/,
        linkedin: /^https:\/\/(www\.)?linkedin.com\/in\/[a-zA-Z0-9-]+$/,
        pinterest: /^https:\/\/(www\.)?pinterest.com\/[a-zA-Z0-9_]+\/?$/,
        reddit: /^https:\/\/(www\.)?reddit.com\/user\/[a-zA-Z0-9_]+$/,
        tiktok: /^https:\/\/(www\.)?tiktok.com\/@?[a-zA-Z0-9_.]+$/,
        twitter: /^https:\/\/(www\.)?twitter.com\/[a-zA-Z0-9_]+$/,
        vimeo: /^https:\/\/(www\.)?vimeo.com\/[a-zA-Z0-9]+$/,
        whatsapp: /^https:\/\/wa.me\/\d+$/,
        youtube: /^https:\/\/(www\.)?youtube.com\/(user|channel)\/[a-zA-Z0-9_-]+$/,
    };
    
    const phonePattern = /^\+?\d{1,4}[-.\s]?(\(?\d{1,3}?\))?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;

    const facebookInput = document.getElementById('facebook').value;
    const instagramInput = document.getElementById('instagram').value;
    const linkedinInput = document.getElementById('linkedin').value;
    const pinterestInput = document.getElementById('pinterest').value;
    const redditInput = document.getElementById('reddit').value;
    const tiktokInput = document.getElementById('tiktok').value;
    const twitterInput = document.getElementById('twitter').value;
    const vimeoInput = document.getElementById('vimeo').value;
    const youtubeInput = document.getElementById('youtube').value;

    const inputs = [
        { value: facebookInput, pattern: urlPatterns.facebook, field: 'Facebook' },
        { value: instagramInput, pattern: urlPatterns.instagram, field: 'Instagram' },
        { value: linkedinInput, pattern: urlPatterns.linkedin, field: 'LinkedIn' },
        { value: pinterestInput, pattern: urlPatterns.pinterest, field: 'Pinterest' },
        { value: redditInput, pattern: urlPatterns.reddit, field: 'Reddit' },
        { value: tiktokInput, pattern: urlPatterns.tiktok, field: 'TikTok' },
        { value: twitterInput, pattern: urlPatterns.twitter, field: 'Twitter' },
        { value: vimeoInput, pattern: urlPatterns.vimeo, field: 'Vimeo' },
        { value: youtubeInput, pattern: urlPatterns.youtube, field: 'YouTube' },
    ];

    let isValid = true;
    
    inputs.forEach(input => {
        if (input.value && !input.pattern.test(input.value.removeTrailingSlash())) {
            alert(`${input.field} URL is invalid`);
            isValid = false;
        }
    });
    return isValid;
}
