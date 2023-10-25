class aguarde {
    constructor() {
        this.telaAcima = document.createElement('div');

        this.telaAcima.style.position = 'absolute';
        this.telaAcima.style.display = 'flex';
        this.telaAcima.style.justifyContent = 'center';
        this.telaAcima.style.alignContent = 'center';
        this.telaAcima.style.top = '0px';
        this.telaAcima.style.left = '0px';
        this.telaAcima.style.height = '100%';
        this.telaAcima.style.width = '100%';
        this.telaAcima.style.backgroundColor = 'gray';
        this.telaAcima.style.opacity = 0.5;
        this.telaAcima.style.zIndex = 100;
        this.telaAcima.style.textAlign = 'center';
        this.telaAcima.style.padding = "25% 0"
        this.telaAcima.style.visibility = 'hidden';
        this.telaAcima.style.overflow = 'hidden';
        
        this.telaAcima.innerHTML = '<spam style="color:white; font-size:200%">Por favor aguarde</spam>'

        document.body.appendChild(this.telaAcima);
    }

    show() {
        this.telaAcima.style.visibility = 'visible';
    }

    hide() {
        this.telaAcima.remove();
    }
}