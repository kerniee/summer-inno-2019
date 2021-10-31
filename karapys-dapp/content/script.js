window.addEventListener('load', async () => {
    window.web3 = new Web3(window.ethereum);
    if (window.ethereum) {
        try {
            await ethereum.enable()
        } catch (error) {
            alert('Э, доступ дал!')
        }

        button = document.getElementById('update-button');
        blockSpan = document.getElementById('block');

        button.addEventListener('click', async() => {
            web3.eth.getBlockNumber(function(err, blockNumber) {
                blockSpan.textContent = blockNumber;
            });
        });
    } else {
        alert('Метамаск скачал!')
    }
});