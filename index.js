const express = require('express');
const { Connection, Request } = require('tedious');
const app = express();
const port = process.env.PORT || 3000;

// Configuración de la base de datos
const config = {
    server: 'dss-retail-srv-[tu-nombre].database.windows.net', 
    authentication: {
        type: 'default',
        options: {
            userName: 'sqladmin',
            password: 'DssRetail2024!'
        }
    },
    options: {
        database: 'dss-retail-db',
        encrypt: true,
        trustServerCertificate: false
    }
};

app.get('/api/recomendacion', (req, res) => {
    const id = req.query.id;
    if (!id) return res.status(400).send('Falta el ID del producto');

    const connection = new Connection(config);
    connection.on('connect', (err) => {
        if (err) return res.status(500).send(err.message);

        const request = new Request(
            `SELECT nombre, stock_actual, unidades_vendidas FROM Vista_Analisis_DSS WHERE id_producto = ${id}`,
            (err, rowCount) => {
                if (err) res.status(500).send(err.message);
                connection.close();
            }
        );

        request.on('row', (columns) => {
            const data = {
                nombre: columns[0].value,
                stock: columns[1].value,
                ventas: columns[2].value
            };
            
            // Lógica DSS
            let recomendacion = "ESTADO NORMAL";
            if (data.stock > 30 && data.ventas < 5) {
                recomendacion = "PROMOCIÓN: Stock alto, baja rotación. Aplicar 20% dcto.";
            } else if (data.stock < 10) {
                recomendacion = "REBASTECIMIENTO: Stock crítico.";
            }

            res.json({ ...data, recomendacion_dss: recomendacion });
        });

        connection.execSql(request);
    });
    connection.connect();
});

app.listen(port, () => console.log(`DSS API escuchando en puerto ${port}`));
