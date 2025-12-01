(function() {

    class ECGPulse {
      constructor() {
        this.demo = document.getElementById('demo');
        this.ctx = this.demo.getContext('2d');
        this.w = this.demo.getBoundingClientRect().width;
        this.h = this.demo.getBoundingClientRect().height;

        this.px = 0;
        this.opx = 0;
        this.py = this.h / 2;
        this.targetPy = this.py;
        this.opy = this.py;

        this.speed = 0.5;
        this.scanBarWidth = 20;
        this.frame = null;

        this.demo.width = this.w;
        this.demo.height = this.h;

        this.ctx.strokeStyle = '#a60f0f';
        this.ctx.lineWidth = 2.0;
        this.ctx.shadowColor = 'rgba(0,255,0,0.9)';
        this.ctx.shadowBlur = 15;

        this.loop = () => {
          this.px += this.speed;

          this.ctx.clearRect(this.px, 0, this.scanBarWidth, this.h);

          this.py += (this.targetPy - this.py) * 0.08;

          this.ctx.beginPath();
          this.ctx.moveTo(this.opx, this.opy);
          this.ctx.lineTo(this.px, this.py);
          this.ctx.stroke();

          this.opx = this.px;
          this.opy = this.py;

          if (this.opx > this.w) {
            this.px = this.opx = -this.speed;
          }

          this.frame = requestAnimationFrame(this.loop);
        };

        this.frame = requestAnimationFrame(this.loop);
      }
    }

    var ecg = new ECGPulse();

    window.addEventListener('nuoviDati', (e) => {
      const { potenza } = e.detail;
      const maxKw = 3;

      let norm = potenza / maxKw;
      norm = Math.max(0, Math.min(1, norm));

      ecg.targetPy = (ecg.h / 2) - (norm - 0.5) * 160;
    });

}());